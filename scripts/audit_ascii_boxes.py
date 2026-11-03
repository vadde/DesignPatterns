#!/usr/bin/env python3
"""
==============================================================================
audit_ascii_boxes.py — Unicode / ASCII Box-Drawing Alignment Linter & Formatter
==============================================================================
Validates and automatically aligns monospace ASCII/Unicode box-drawing tables,
cards, and diagrams across all documentation markdown files.

Handles:
- Visual display width computation per Unicode UAX #11 (East Asian Width).
- Wide characters & emojis (e.g. 🟢, 🚗, 🛑, 🎯, ✅, 💥) having width 2.
- Zero-width modifiers (e.g. \uFE0F variation selector, \u200D ZWJ).
- Single-column box cards (┌─...─┐, │...│, └─...─┘).
- Multi-column box tables (┌─┬─┐, │...│...│, ├─┼─┤, └─┴─┘).
- Subgraph connectors (└─┬─┘, └─┴─┘).

CLI Usage:
    python3 scripts/audit_ascii_boxes.py --check          # Validate in CI / pre-commit
    python3 scripts/audit_ascii_boxes.py --fix            # Auto-align in place
    python3 scripts/audit_ascii_boxes.py path/to/file.md  # Target specific file
"""

import os
import sys
import re
import argparse
import unicodedata
from typing import List, Tuple, Optional


def char_display_width(ch: str) -> int:
    """Return the monospace visual display column width of a single character."""
    # Zero-width characters (variation selectors, combining marks, format chars)
    if ch in ('\ufe0f', '\ufe0e', '\u200d', '\u200b', '\u200c', '\u200e', '\u200f'):
        return 0
    cp = ord(ch)
    if unicodedata.category(ch) in ('Mn', 'Me', 'Cf'):
        return 0
    # Explicit East Asian Wide or Fullwidth
    ea = unicodedata.east_asian_width(ch)
    if ea in ('W', 'F'):
        return 2
    # Standard emoji ranges that render as 2 columns in terminal & monospace browser fonts
    if 0x1F000 <= cp <= 0x1FAFF:
        return 2
    # Specific common 2-column emojis in Miscellaneous & Dingbats (2600-27BF)
    if ch in ('✅', '⚡', '⚠️', '☕', '⚓', '⏳', '⌛', '⏰', '⏱', '⏲', '✂', '✈', '✉', '✏', '✒', '❌', '❎', '❓', '❔', '❕', '❗', '❤', '💔', '⭐', '🌟'):
        return 2
    # Mathematical long double arrow ⟹ (0x27F9)
    if cp == 0x27F9:
        return 2
    return 1


def str_display_width(s: str) -> int:
    """Compute the total monospace visual display width of a string."""
    return sum(char_display_width(ch) for ch in s)


def is_box_top(line: str) -> bool:
    s = line.strip()
    return s.startswith('┌') and s.endswith('┐') and '─' in s


def is_box_bottom(line: str) -> bool:
    s = line.strip()
    return s.startswith('└') and s.endswith('┘') and ('─' in s or '═' in s)


def is_box_middle(line: str) -> bool:
    s = line.strip()
    return (s.startswith('│') and s.endswith('│')) or (s.startswith('├') and s.endswith('┤'))


def align_single_column_box(box_lines: List[str]) -> List[str]:
    """Realign a single-column box (e.g. callout card, definition pill, pillar)."""
    if not box_lines:
        return box_lines

    indent_len = len(box_lines[0]) - len(box_lines[0].lstrip())
    indent_str = box_lines[0][:indent_len]

    max_body_w = 0
    for line in box_lines:
        s = line.strip()
        if s.startswith('│') and s.endswith('│'):
            body = s[1:-1]
            bw = str_display_width(body.rstrip())
            if bw > max_body_w:
                max_body_w = bw

    # Determine target content width
    top_stripped = box_lines[0].strip()
    top_dashes = str_display_width(top_stripped[1:-1])
    target_w = max(top_dashes, max_body_w + 1)

    new_lines = []
    for line in box_lines:
        s = line.strip()
        if s.startswith('┌') and s.endswith('┐'):
            new_lines.append(indent_str + '┌' + ('─' * target_w) + '┐')
        elif s.startswith('├') and s.endswith('┤'):
            new_lines.append(indent_str + '├' + ('─' * target_w) + '┤')
        elif s.startswith('└') and s.endswith('┘'):
            # Preserve special connectors like ┴ or ┬ if present
            if '┬' in s or '┴' in s:
                conn = '┬' if '┬' in s else '┴'
                half = (target_w - 1) // 2
                rem = target_w - 1 - half
                new_lines.append(indent_str + '└' + ('─' * half) + conn + ('─' * rem) + '┘')
            else:
                new_lines.append(indent_str + '└' + ('─' * target_w) + '┘')
        elif s.startswith('│') and s.endswith('│'):
            body = s[1:-1]
            body_trimmed = body.rstrip()
            pad = target_w - str_display_width(body_trimmed)
            if pad < 0:
                pad = 0
            new_lines.append(indent_str + '│' + body_trimmed + (' ' * pad) + '│')
        else:
            new_lines.append(line)

    return new_lines


def align_multi_column_box(box_lines: List[str]) -> List[str]:
    """Realign a multi-column box table (e.g. system comparisons, triage tables)."""
    if not box_lines:
        return box_lines

    indent_len = len(box_lines[0]) - len(box_lines[0].lstrip())
    indent_str = box_lines[0][:indent_len]

    # Find number of columns from lines with │
    num_cols = 0
    for line in box_lines:
        s = line.strip()
        if s.startswith('│') and s.endswith('│'):
            parts = s[1:-1].split('│')
            num_cols = max(num_cols, len(parts))

    if num_cols <= 1:
        return align_single_column_box(box_lines)

    # Determine max needed width for each column
    col_widths = [0] * num_cols

    # First check existing border splits
    for line in box_lines:
        s = line.strip()
        if (s.startswith('┌') and '┬' in s) or (s.startswith('├') and '┼' in s) or (s.startswith('└') and '┴' in s):
            parts = re.split(r'[┌┬┐├┼┤└┴┘]', s)[1:-1]
            if len(parts) == num_cols:
                for i, p in enumerate(parts):
                    col_widths[i] = max(col_widths[i], str_display_width(p))

    # Next check content cells
    for line in box_lines:
        s = line.strip()
        if s.startswith('│') and s.endswith('│'):
            parts = s[1:-1].split('│')
            if len(parts) == num_cols:
                for i, p in enumerate(parts):
                    w = str_display_width(p.rstrip()) + 1
                    col_widths[i] = max(col_widths[i], w)

    new_lines = []
    for line in box_lines:
        s = line.strip()
        if s.startswith('┌') and s.endswith('┐'):
            new_lines.append(indent_str + '┌' + '┬'.join('─' * w for w in col_widths) + '┐')
        elif s.startswith('├') and s.endswith('┤'):
            new_lines.append(indent_str + '├' + '┼'.join('─' * w for w in col_widths) + '┤')
        elif s.startswith('└') and s.endswith('┘'):
            new_lines.append(indent_str + '└' + '┴'.join('─' * w for w in col_widths) + '┘')
        elif s.startswith('│') and s.endswith('│'):
            parts = s[1:-1].split('│')
            if len(parts) == num_cols:
                new_parts = []
                for i, p in enumerate(parts):
                    trimmed = p.rstrip()
                    pad = col_widths[i] - str_display_width(trimmed)
                    if pad < 0:
                        pad = 0
                    new_parts.append(trimmed + (' ' * pad))
                new_lines.append(indent_str + '│' + '│'.join(new_parts) + '│')
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return new_lines


def process_file_content(content: str, fix: bool = False) -> Tuple[str, List[dict]]:
    """
    Parse and optionally align all box-drawing blocks in a markdown file.
    Returns (updated_content, list_of_box_reports).
    """
    lines = content.split('\n')
    reports = []
    new_all_lines = []
    
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        
        # Check if line is the start of a box
        if is_box_top(line):
            box_start_idx = i
            box_lines = [line]
            j = i + 1
            is_valid_box = False
            
            while j < n:
                curr = lines[j]
                box_lines.append(curr)
                if is_box_bottom(curr):
                    is_valid_box = True
                    break
                elif is_box_middle(curr) or is_box_top(curr):
                    j += 1
                else:
                    # Non-box line encountered before bottom border
                    break
            
            if is_valid_box:
                box_end_idx = j
                widths = [str_display_width(bl) for bl in box_lines]
                is_misaligned = len(set(widths)) > 1
                
                reports.append({
                    'start_line': box_start_idx + 1,
                    'end_line': box_end_idx + 1,
                    'is_misaligned': is_misaligned,
                    'widths': widths,
                    'box_lines': box_lines
                })
                
                if fix and is_misaligned:
                    # Decide single vs multi-column
                    has_col_dividers = any(('┬' in bl or '┼' in bl or '┴' in bl or (bl.strip().startswith('│') and bl.strip()[1:-1].count('│') > 0)) for bl in box_lines)
                    if has_col_dividers:
                        aligned = align_multi_column_box(box_lines)
                    else:
                        aligned = align_single_column_box(box_lines)
                    new_all_lines.extend(aligned)
                else:
                    new_all_lines.extend(box_lines)
                
                i = box_end_idx + 1
                continue
        
        new_all_lines.append(line)
        i += 1

    updated_content = '\n'.join(new_all_lines)
    return updated_content, reports


def collect_target_files(paths: Optional[List[str]] = None) -> List[str]:
    """Gather all candidate markdown files across the repository."""
    if paths:
        targets = []
        for p in paths:
            if os.path.isfile(p):
                targets.append(p)
            elif os.path.isdir(p):
                for root, dirs, files in os.walk(p):
                    if any(skip in root for skip in ('.git', '_site', 'node_modules', '.gemini')):
                        continue
                    for f in files:
                        if f.endswith('.md'):
                            targets.append(os.path.join(root, f))
        return sorted(list(set(targets)))

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    targets = []
    for root, dirs, files in os.walk(root_dir):
        if any(skip in root for skip in ('.git', '_site', 'node_modules', '.gemini')):
            continue
        for f in files:
            if f.endswith('.md'):
                targets.append(os.path.join(root, f))
    return sorted(targets)


def main():
    parser = argparse.ArgumentParser(description="Audit and format Unicode ASCII box-drawing tables & cards.")
    parser.add_argument('paths', nargs='*', help="File or directory paths to audit")
    parser.add_argument('--fix', action='store_true', help="Automatically format and align misaligned boxes in place")
    parser.add_argument('--check', action='store_true', help="Validate alignment and exit with code 1 on failure")
    args = parser.parse_args()

    files = collect_target_files(args.paths if args.paths else None)
    
    total_boxes = 0
    misaligned_boxes = 0
    fixed_files = 0
    
    print("╔══════════════════════════════════════════════════════════════════╗")
    print(f"║  📐 Unicode Monospace Box-Drawing Alignment Linter & Formatter  ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    for fpath in files:
        rel_path = os.path.relpath(fpath, os.getcwd())
        try:
            with open(fpath, 'r', encoding='utf-8') as fp:
                original = fp.read()
        except Exception:
            continue
        
        if '┌' not in original:
            continue
            
        updated, reports = process_file_content(original, fix=args.fix)
        file_has_misalignment = False
        
        for r in reports:
            total_boxes += 1
            if r['is_misaligned']:
                misaligned_boxes += 1
                file_has_misalignment = True
                w_set = set(r['widths'])
                print(f"  ❌ [{rel_path}:{r['start_line']}-{r['end_line']}] Misaligned box widths: {w_set}")
                if not args.fix:
                    for idx, line in enumerate(r['box_lines']):
                        w = str_display_width(line)
                        print(f"     L{r['start_line'] + idx:3d} (w={w:2d}): {line}")
        
        if args.fix and file_has_misalignment:
            with open(fpath, 'w', encoding='utf-8') as fp:
                fp.write(updated)
            fixed_files += 1
            print(f"  ✨ Fixed and realigned boxes in {rel_path}")

    print("\n------------------------------------------------------------------")
    print(f"Summary: Audited {total_boxes} boxes across {len(files)} files.")
    if misaligned_boxes == 0:
        print("✅ 100% of ASCII/Unicode box-drawing tables and cards are perfectly aligned!")
        sys.exit(0)
    else:
        if args.fix:
            print(f"🎉 Realigned {misaligned_boxes} boxes across {fixed_files} files.")
            sys.exit(0)
        else:
            print(f"⚠️ Found {misaligned_boxes} misaligned box blocks.")
            if args.check:
                sys.exit(1)
            sys.exit(0)


if __name__ == '__main__':
    main()

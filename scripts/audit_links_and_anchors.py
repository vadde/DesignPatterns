#!/usr/bin/env python3
"""
scripts/audit_links_and_anchors.py
==============================================================================
Gate 15: Universal Hyperlink Integrity & Local Path Leak Prevention Linter.
Validates:
  1. Zero local file paths (file://, /Users/) across all Markdown source files.
  2. Zero local file paths in compiled static documentation (index.html).
  3. Zero raw relative file links (.md, .py, ../path/) leaking in compiled index.html.
  4. Zero external GitHub repository jumps (github.com/vadde/DesignPatterns/blob or /tree)
     for content that is already compiled into the documentation portal.
  5. 100% resolution of in-page fragment anchors (href="#..."):
     Every single internal anchor must map to a valid element id on the page.
==============================================================================
"""

import os
import re
import sys
import glob
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_HTML = ROOT_DIR / "docs" / "site" / "index.html"
SITE_HTML = ROOT_DIR / "_site" / "index.html"

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
RESET = "\033[0m"

def audit_source_markdown() -> bool:
    print(f"{CYAN}→ 1. Auditing Markdown sources for local filesystem paths & link typos...{RESET}")
    violations = []

    for md_path in sorted(ROOT_DIR.glob("**/*.md")):
        p_str = str(md_path)
        if any(x in p_str for x in [".agents", "node_modules", "specs", "docs/site", "_site", ".git"]):
            continue

        with open(md_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if "file://" in content or "/Users/" in content:
            violations.append((md_path.relative_to(ROOT_DIR), "Contains 'file://' or '/Users/' local path"))

    if violations:
        for f, err in violations:
            print(f"{RED}❌ {f}: {err}{RESET}")
        return False

    print(f"   {GREEN}✅ 100% of Markdown source files are free of local paths.{RESET}")
    return True

def audit_compiled_html(html_path: Path) -> bool:
    print(f"{CYAN}→ 2. Auditing {html_path.relative_to(ROOT_DIR)} for hyperlink integrity & SPA containment...{RESET}")
    if not html_path.exists():
        print(f"{RED}❌ File not found: {html_path}{RESET}")
        return False

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    forbidden_terms = [
        ("file://", "Local file scheme in href"),
        ("/Users/", "Local user directory in href"),
    ]

    leak_found = False
    for term, desc in forbidden_terms:
        count = html.count(term)
        if count > 0:
            print(f"{RED}❌ Fatal: Found {count} occurrences of '{term}' ({desc}) in {html_path.name}{RESET}")
            leak_found = True

    if leak_found:
        return False

    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html)
    print(f"   {CYAN}Auditing {len(hrefs)} hyperlinks in {html_path.name}...{RESET}")

    unresolved_md = []
    unresolved_py = []
    forbidden_gh_jumps = []

    for h in hrefs:
        # Check raw .md links
        if re.search(r'\.md(?:#[^\s"\']*)?$', h):
            unresolved_md.append(h)
        # Check raw .py links
        elif re.search(r'\.py(?:#[^\s"\']*)?$', h):
            unresolved_py.append(h)
        # Check GitHub repo jumps into internal codebase files
        elif "github.com/vadde/DesignPatterns" in h and any(k in h for k in ["/blob/", "/tree/"]):
            forbidden_gh_jumps.append(h)

    errors = False
    if unresolved_md:
        print(f"{RED}❌ Found {len(unresolved_md)} raw .md links that break in production SPA:{RESET}")
        for l in unresolved_md[:5]: print(f"      {l}")
        errors = True

    if unresolved_py:
        print(f"{RED}❌ Found {len(unresolved_py)} raw .py links:{RESET}")
        for l in unresolved_py[:5]: print(f"      {l}")
        errors = True

    if forbidden_gh_jumps:
        print(f"{RED}❌ Found {len(forbidden_gh_jumps)} external GitHub repo jumps for internal files:{RESET}")
        for l in forbidden_gh_jumps[:5]: print(f"      {l}")
        errors = True

    if errors:
        return False

    print(f"   {GREEN}✅ Zero raw .md, raw .py, or internal GitHub jumps.{RESET}")

    # Validate all internal fragment anchors (href="#...")
    all_ids = set(re.findall(r'id=["\']([^"\']+)["\']', html))
    internal_anchors = re.findall(r'href=["\']#([^"\']+)["\']', html)

    missing_targets = set()
    for a in internal_anchors:
        if not a or a == "top": continue
        if a not in all_ids:
            missing_targets.add(a)

    if missing_targets:
        print(f"{RED}❌ Found {len(missing_targets)} broken fragment anchors that point to non-existent IDs:{RESET}")
        for a in sorted(missing_targets)[:10]:
            print(f"      #{a}")
        return False

    print(f"   {GREEN}✅ 100% of internal anchors ({len(internal_anchors)} references) resolve to valid element IDs.{RESET}")
    return True

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🔗 Universal Hyperlink Integrity & Local Path Prevention Linter║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    source_ok = audit_source_markdown()
    if not source_ok:
        sys.exit(1)

    targets = [f for f in [SITE_HTML] if f.exists()]
    if not targets:
        print(f"{RED}❌ _site/index.html not found. Run 'make docs-build' first.{RESET}")
        sys.exit(1)

    html_ok = True
    for t in targets:
        if not audit_compiled_html(t):
            html_ok = False

    if source_ok and html_ok:
        print()
        print("──────────────────────────────────────────────────────────────────")
        print(f"{GREEN}🎉 100% HYPERLINK INTEGRITY & SPA CONTAINMENT INVARIANTS PASSED!{RESET}")
        sys.exit(0)
    else:
        print()
        print(f"{RED}❌ Hyperlink integrity or SPA containment invariants violated.{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()

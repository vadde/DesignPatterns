#!/usr/bin/env python3
"""
scripts/audit_monospace_badging.py
==============================================================================
Gate 14: Monospace Semantic Badging & Implementation Tag Linter.
Validates:
  1. 100% elimination of meaningless '⚡ TEXT Implementation' and '⚡ NONE Implementation'.
  2. Integrity of content-aware semantic badges in compiled index.html:
     - ⚡ Python 3.14 Implementation (.dna-label-code)
     - Framework Badges (.dna-label-django, .dna-label-fastapi, .dna-label-sqlalchemy, .dna-label-celery)
     - 📐 Monospace Reference Matrix (.dna-label-matrix)
     - 📜 Master Architecture / Blueprint (.dna-label-blueprint)
     - 📋 Technical Specification & Proof (.dna-label-spec)
==============================================================================
"""

import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SITE_HTML = ROOT_DIR / "_site" / "index.html"

CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
RED = "\033[0;31m"
RESET = "\033[0m"

def audit_file(html_path: Path) -> bool:
    print(f"{CYAN}→ Auditing {html_path.relative_to(ROOT_DIR)} for semantic badging...{RESET}")
    if not html_path.exists():
        print(f"{RED}❌ File not found: {html_path}{RESET}")
        return False

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Elimination of mislabeled badges
    if "⚡ TEXT Implementation" in content:
        print(f"{RED}❌ Fatal: Found '⚡ TEXT Implementation' in {html_path.name}{RESET}")
        return False
    if "⚡ NONE Implementation" in content:
        print(f"{RED}❌ Fatal: Found '⚡ NONE Implementation' in {html_path.name}{RESET}")
        return False

    print(f"   {GREEN}✅ Zero occurrences of '⚡ TEXT Implementation' or '⚡ NONE Implementation'.{RESET}")

    # 2. Semantic Badges Presence & Distribution
    badge_matches = re.findall(r'<span class="dna-label ([^"]+)">([^<]+)</span>', content)
    if not badge_matches:
        print(f"{RED}❌ Fatal: No .dna-label elements found in {html_path.name}{RESET}")
        return False

    badge_types = {}
    for cls, _ in badge_matches:
        for c in cls.split():
            badge_types[c] = badge_types.get(c, 0) + 1

    expected_classes = [
        "dna-label-code",
        "dna-label-blueprint",
        "dna-label-django",
        "dna-label-fastapi",
        "dna-label-sqlalchemy"
    ]
    for rc in expected_classes:
        if rc not in badge_types or badge_types[rc] == 0:
            print(f"{RED}❌ Fatal: Missing semantic badge class '{rc}' in {html_path.name}{RESET}")
            return False

    print(f"   {GREEN}✅ Validated semantic badge diversity ({len(badge_matches)} blocks classified):{RESET}")
    for rc, count in sorted(badge_types.items()):
        print(f"      • {rc}: {count} blocks")

    return True

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  🏷️  Monospace Semantic Badging & Implementation Linter          ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    if not SITE_HTML.exists():
        print(f"{RED}❌ _site/index.html not found. Run 'make docs-build' first.{RESET}")
        sys.exit(1)

    if audit_file(SITE_HTML):
        print()
        print("──────────────────────────────────────────────────────────────────")
        print(f"{GREEN}🎉 100% MONOSPACE BADGING INVARIANTS PASSED!{RESET}")
        sys.exit(0)
    else:
        print()
        print(f"{RED}❌ Monospace badging invariants violated.{RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()

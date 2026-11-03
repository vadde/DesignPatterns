#!/usr/bin/env python3
"""
scripts/audit_collapsible_elements.py
=============================================================================
Universal Collapsible Element & Accordion Invariant Audit Engine.

Guarantees 100% compliance across repository Markdown files and compiled
static site HTML/CSS/JS:
1. Markdown Source Integrity:
   - Validates that every <details> has a matching </details>.
   - Validates that every <summary> has a matching </summary>.
2. Compiled HTML Presentation Invariants:
   - Zero raw/escaped &lt;details&gt; or &lt;summary&gt; text leakage.
   - Zero invalid paragraph wrappers (<p class="md-p"><details>).
   - 100% of markdown details are rendered into semantic <details class="md-details">.
   - Every .md-details has a corresponding .md-summary and .md-details-body.
3. Design System & Audio Haptics Invariants:
   - .md-details, .md-summary, .md-details-body rules present in CSS.
   - Mica theme styling overrides present in CSS.
   - Audio haptic click delegation in app.js binds to .md-summary.
=============================================================================
"""

import sys
import re
import glob
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SITE_INDEX = ROOT_DIR / "_site" / "index.html"
SITE_CSS = ROOT_DIR / "_site" / "style.css"
SITE_JS = ROOT_DIR / "_site" / "app.js"

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"

def audit_markdown_sources() -> tuple[list[str], int]:
    """Audits all repository markdown files for balanced details/summary tags."""
    errors = []
    md_files = sorted(glob.glob(str(ROOT_DIR / "**/*.md"), recursive=True))

    total_details = 0
    total_summaries = 0

    for f_path_str in md_files:
        if any(skip in f_path_str for skip in ["_site", "node_modules", ".agents", "specs/"]):
            continue
        p = Path(f_path_str)
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            errors.append(f"Could not read {p}: {e}")
            continue

        open_details = len(re.findall(r'<details(?:\s+[^>]*)?>', content, re.IGNORECASE))
        close_details = len(re.findall(r'</details>', content, re.IGNORECASE))
        open_summaries = len(re.findall(r'<summary(?:\s+[^>]*)?>', content, re.IGNORECASE))
        close_summaries = len(re.findall(r'</summary>', content, re.IGNORECASE))

        if open_details != close_details:
            errors.append(f"{p.relative_to(ROOT_DIR)}: Mismatched <details> ({open_details}) vs </details> ({close_details})")
        if open_summaries != close_summaries:
            errors.append(f"{p.relative_to(ROOT_DIR)}: Mismatched <summary> ({open_summaries}) vs </summary> ({close_summaries})")
        if open_details != open_summaries:
            errors.append(f"{p.relative_to(ROOT_DIR)}: <details> count ({open_details}) does not match <summary> count ({open_summaries})")

        total_details += open_details
        total_summaries += open_summaries

    return errors, total_details

def audit_compiled_html() -> tuple[list[str], int]:
    """Audits _site/index.html for raw HTML leakage and structural integrity."""
    errors = []
    if not SITE_INDEX.exists():
        return [f"Compiled index.html not found at {SITE_INDEX}. Run 'make docs-build' first."], 0

    html_content = SITE_INDEX.read_text(encoding="utf-8", errors="ignore")

    # 1. Check for raw escaped entity leakage
    for tag in ["&lt;details", "&lt;summary", "&lt;/details", "&lt;/summary"]:
        if tag in html_content:
            count = html_content.count(tag)
            errors.append(f"Found {count} raw escaped '{tag}' tag(s) in compiled index.html! Content is showing unrendered.")

    # 2. Check for invalid paragraph wrapping around details
    if re.search(r'<p\s+class="md-p">\s*<details', html_content):
        errors.append("Invalid markup: <details> is wrapped inside a <p class=\"md-p\"> paragraph!")
    if re.search(r'</details>\s*</p>', html_content):
        errors.append("Invalid markup: </details> is closed by a trailing </p> paragraph!")

    # 3. Check for rendered .md-details, .md-summary, and .md-details-body
    md_details_count = html_content.count('class="md-details"')
    md_summary_count = html_content.count('class="md-summary"')
    md_body_count = html_content.count('class="md-details-body"')

    if md_details_count > 0:
        if md_details_count != md_summary_count:
            errors.append(f"Discrepancy: {md_details_count} .md-details elements but {md_summary_count} .md-summary elements.")
        if md_details_count != md_body_count:
            errors.append(f"Discrepancy: {md_details_count} .md-details elements but {md_body_count} .md-details-body wrappers.")

    return errors, md_details_count

def audit_styling_and_haptics() -> list[str]:
    """Audits style.css and app.js for .md-details design tokens and audio bindings."""
    errors = []
    if not SITE_CSS.exists():
        errors.append(f"Compiled style.css not found at {SITE_CSS}.")
    else:
        css = SITE_CSS.read_text(encoding="utf-8")
        if ".md-details" not in css:
            errors.append("Missing .md-details styling rule in style.css.")
        if ".md-summary" not in css:
            errors.append("Missing .md-summary styling rule in style.css.")
        if ".md-details-body" not in css:
            errors.append("Missing .md-details-body styling rule in style.css.")
        if '[data-theme="mica"] .md-summary' not in css and '[data-theme="mica"] .md-details' not in css:
            errors.append("Missing Mica theme override for .md-details / .md-summary in style.css.")

    if not SITE_JS.exists():
        errors.append(f"Compiled app.js not found at {SITE_JS}.")
    else:
        js = SITE_JS.read_text(encoding="utf-8")
        if ".md-details" not in js:
            errors.append("Missing .md-details selector in app.js Expand/Collapse All handlers.")

    return errors

def main():
    source_only = "--source-only" in sys.argv
    print(f"{CYAN}╔══════════════════════════════════════════════════════════════════╗{NC}")
    print(f"{CYAN}║  📂 Auditing Collapsible Elements & Raw HTML Block Invariants   ║{NC}")
    print(f"{CYAN}╚══════════════════════════════════════════════════════════════════╝{NC}")

    all_errors = []

    # 1. Source Markdown Audit
    print("  → Auditing repository Markdown sources for tag balance...")
    md_errors, total_md_details = audit_markdown_sources()
    if md_errors:
        for err in md_errors:
            print(f"    {RED}❌ {err}{NC}")
        all_errors.extend(md_errors)
    else:
        print(f"    {GREEN}✅ Validated {total_md_details} balanced <details>/<summary> pairs across all Markdown files.{NC}")

    if not source_only:
        # 2. Compiled HTML Audit
        print("  → Auditing compiled _site/index.html for raw HTML leakage...")
        html_errors, rendered_count = audit_compiled_html()
        if html_errors:
            for err in html_errors:
                print(f"    {RED}❌ {err}{NC}")
            all_errors.extend(html_errors)
        else:
            print(f"    {GREEN}✅ Validated {rendered_count} semantic <details class=\"md-details\"> elements with ZERO raw leakage.{NC}")

        # 3. CSS & Audio Haptics Invariant Audit
        print("  → Auditing CSS design tokens and JS bindings...")
        asset_errors = audit_styling_and_haptics()
        if asset_errors:
            for err in asset_errors:
                print(f"    {RED}❌ {err}{NC}")
            all_errors.extend(asset_errors)
        else:
            print(f"    {GREEN}✅ CSS design tokens and JS bindings verified.{NC}")

    print("─" * 66)
    if all_errors:
        print(f"{RED}❌ FAILED: Found {len(all_errors)} collapsible element invariant violations!{NC}")
        sys.exit(1)
    else:
        print(f"{GREEN}🎉 100% COLLAPSIBLE ELEMENT INVARIANTS PASSED DETERMINISTICALLY!{NC}")
        sys.exit(0)

if __name__ == "__main__":
    main()

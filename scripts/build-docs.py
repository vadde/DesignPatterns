#!/usr/bin/env python3
"""
==============================================================================
build-docs.py — Zero-Dependency Design Patterns Living Documentation Compiler
Compiles 28 chapters, 5 architectural tiers, 38 Python 3.14 implementations,
and 84 Mermaid diagrams into a futuristic Year 2500 Command Deck static site.
Features full Markdown-to-HTML rendering, interactive code workbenches,
fullscreen theater modal, and deep search indexing.
==============================================================================
"""

import os
import re
import sys
import json
import html
import shutil
import urllib.parse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_SITE_DIR = ROOT_DIR / "docs" / "site"
SITE_DIR = ROOT_DIR / "_site"
CATALOG_DIR = SITE_DIR / "catalog"

TIERS = {
    "Foundations": {
        "icon": "🏗️",
        "tagline": "First Principles & Foundations",
        "desc": "Object-oriented first principles, SOLID, Composition vs Inheritance, and UML primer.",
        "patterns": ["00 - Foundations"],
    },
    "Creational": {
        "icon": "🔨",
        "tagline": "Creational Patterns",
        "desc": "How objects are created — controlling instantiation to keep systems decoupled and flexible.",
        "patterns": [
            "01 - Singleton (Creational)",
            "02 - Factory Method (Creational)",
            "03 - Abstract Factory (Creational)",
            "04 - Builder (Creational)",
            "05 - Prototype (Creational)",
        ],
    },
    "Structural": {
        "icon": "🧱",
        "tagline": "Structural Patterns",
        "desc": "How objects are composed — assembling larger, resilient structures from individual parts.",
        "patterns": [
            "06 - Adapter (Structural)",
            "07 - Bridge (Structural)",
            "08 - Composite (Structural)",
            "09 - Decorator (Structural)",
            "10 - Facade (Structural)",
            "11 - Flyweight (Structural)",
            "12 - Proxy (Structural)",
        ],
    },
    "Behavioral": {
        "icon": "💬",
        "tagline": "Behavioral Patterns",
        "desc": "How objects communicate — defining interaction protocols and responsibility distribution.",
        "patterns": [
            "13 - Chain of Responsibility (Behavioral)",
            "14 - Command (Behavioral)",
            "15 - Iterator (Behavioral)",
            "16 - Mediator (Behavioral)",
            "17 - Memento (Behavioral)",
            "18 - Observer (Behavioral)",
            "19 - State (Behavioral)",
            "20 - Strategy (Behavioral)",
            "21 - Template Method (Behavioral)",
            "22 - Visitor (Behavioral)",
        ],
    },
    "Architectural": {
        "icon": "🚀",
        "tagline": "Architectural & Advanced",
        "desc": "Beyond GoF — patterns that shape enterprise applications, persistence, and state at scale.",
        "patterns": [
            "23 - Repository Pattern (Architectural)",
            "24 - Unit of Work (Architectural)",
            "25 - Dependency Injection (Architectural)",
            "26 - Event Sourcing & CQRS (Architectural)",
        ],
    },
    "Capstone": {
        "icon": "🎯",
        "tagline": "Capstone & Wild Sightings",
        "desc": "Decision matrix, anti-patterns, real-world framework sightings, and interview playbook.",
        "patterns": ["27 - Patterns in the Wild (Capstone)"],
    },
}

def get_tier_for_folder(folder_name: str) -> str:
    for tier, data in TIERS.items():
        if folder_name in data["patterns"]:
            return tier
    return "Architectural"

def slugify(text: str) -> str:
    """Generate a clean URL/anchor slug from a title or folder name."""
    clean = re.sub(r'[\(\)]', '', text)
    clean = re.sub(r'[^\w\s-]', '', clean).strip().lower()
    return re.sub(r'[-\s]+', '-', clean)

def get_chapter_slug(folder_name: str) -> str:
    """e.g. '01 - Singleton (Creational)' -> 'chapter-01-singleton'"""
    m = re.match(r'^(\d{2})\s*-\s*([^(]+)', folder_name)
    if m:
        num = m.group(1)
        name = slugify(m.group(2).strip())
        return f"chapter-{num}-{name}"
    return f"chapter-{slugify(folder_name)}"

_DIAGRAM_COUNTER = 0

def sanitize_mermaid(content: str) -> str:
    """
    Sanitize Mermaid syntax:
    - Escapes unescaped < and > in node labels as &lt; and &gt;
    - Fixes potential label or bracket syntax outliers
    """
    # Replace raw angle brackets inside square bracket labels
    def repl_bracket(m):
        inner = m.group(1)
        # Preserve <br/> and <br>
        inner_clean = re.sub(r'<br\s*/?>', '__BR_PLACEHOLDER__', inner)
        inner_clean = inner_clean.replace('<', '&lt;').replace('>', '&gt;')
        inner_clean = inner_clean.replace('__BR_PLACEHOLDER__', '<br/>')
        return f'[{inner_clean}]'

    content = re.sub(r'\[([^\]\n]+)\]', repl_bracket, content)

    # Enclose unquoted edge labels containing () or [] in quotes
    def repl_edge(m):
        arr = m.group(1)
        lbl = m.group(2).strip()
        if (lbl.startswith('"') and lbl.endswith('"')) or (lbl.startswith("'") and lbl.endswith("'")):
            return m.group(0)
        clean = lbl.replace('"', "'")
        return f'{arr}|"{clean}"|'
    content = re.sub(r'(-->|-.->|==>)\|([^|\n]*[\(\)\[\]][^|\n]*)\|', repl_edge, content)

    return content

def classify_code_block(lang: str, code: str) -> tuple[str, str, str]:
    """Classify a code block into a badge title, CSS class, and language."""
    raw_lang = (lang or "").strip().lower()
    if raw_lang in ("python", "py", "python3"):
        return "⚡ Python 3.14 Implementation", "dna-label-code", "python"
    elif raw_lang in ("json",):
        return "⚡ JSON Schema & Contract", "dna-label-spec", "json"
    elif raw_lang in ("bash", "sh", "shell", "zsh"):
        return "⚡ Shell Command / Script", "dna-label-code", "bash"
    elif raw_lang in ("sql",):
        return "⚡ SQL Schema & Query", "dna-label-code", "sql"
    elif raw_lang in ("tree", "hierarchy"):
        return "🌳 Structural Hierarchy & Topology", "dna-label-tree", "plaintext"
    elif raw_lang in ("matrix", "table", "ascii-table"):
        return "📐 Monospace Reference Matrix", "dna-label-matrix", "plaintext"

    # Heuristic detection
    code_stripped = code.strip()
    if any(box in code_stripped for box in ["┌", "╔", "╒", "+---", "|---"]):
        return "📐 Monospace Reference Matrix", "dna-label-matrix", "plaintext"
    if any(c in code_stripped for c in ["/  \\", "/ \\", "├──", "└──"]):
        return "🌳 Structural Hierarchy & Topology", "dna-label-tree", "plaintext"
    if "def " in code_stripped or "class " in code_stripped or "import " in code_stripped:
        return "⚡ Python 3.14 Implementation", "dna-label-code", "python"

    return "📋 Technical Blueprint & Specification", "dna-label-spec", "plaintext"

def render_markdown(text: str, current_folder: str = "") -> str:
    """
    Converts markdown content into semantic, accessible HTML with:
    - Unique Mermaid diagrams wrapped in theater-enabled workbenches
    - Table touch wrappers with min-width
    - Semantic <details class="md-details"> with <summary class="md-summary">
    - Relative link conversion to in-page hashes
    - Syntax-highlighted code blocks with copy action
    """
    global _DIAGRAM_COUNTER

    # 1. Protect code blocks and mermaid diagrams
    code_blocks = []
    mermaid_blocks = []

    def save_mermaid(m):
        global _DIAGRAM_COUNTER
        _DIAGRAM_COUNTER += 1
        raw_code = m.group(1).strip()
        sanitized = sanitize_mermaid(raw_code)
        diag_id = f"mermaid-diagram-{_DIAGRAM_COUNTER}"
        placeholder = f"___MERMAID_PLACEHOLDER_{len(mermaid_blocks)}___"
        mermaid_blocks.append((diag_id, sanitized))
        return placeholder

    text = re.sub(r'```mermaid\s*\n(.*?)\n```', save_mermaid, text, flags=re.DOTALL)

    def save_code(m):
        lang = m.group(1).strip() if m.group(1) else ""
        code = m.group(2)
        badge_title, badge_cls, prism_lang = classify_code_block(lang, code)
        escaped_code = html.escape(code.rstrip())
        placeholder = f"___CODE_PLACEHOLDER_{len(code_blocks)}___"
        
        rendered = (
            f'<div class="code-container">\n'
            f'  <div class="code-header">\n'
            f'    <span class="dna-label {badge_cls}">{badge_title}</span>\n'
            f'    <button class="copy-btn" title="Copy code to clipboard">Copy</button>\n'
            f'  </div>\n'
            f'  <pre><code class="language-{prism_lang}">{escaped_code}</code></pre>\n'
            f'</div>'
        )
        code_blocks.append(rendered)
        return placeholder

    text = re.sub(r'```([a-zA-Z0-9_-]*)\s*\n(.*?)\n```', save_code, text, flags=re.DOTALL)

    # 2. Convert <details> and <summary> to semantic .md-details and .md-summary
    def repl_details(m):
        inner = m.group(1).strip()
        summary_text = "Answers"
        sum_match = re.search(r'<summary>(.*?)</summary>', inner, flags=re.DOTALL | re.IGNORECASE)
        if sum_match:
            summary_text = sum_match.group(1).strip()
            body_text = inner[sum_match.end():].strip()
        else:
            body_text = inner

        # Recursively render body
        body_html = render_markdown(body_text, current_folder)
        return (
            f'<details class="md-details">\n'
            f'  <summary class="md-summary">{summary_text}</summary>\n'
            f'  <div class="md-details-body">\n{body_html}\n  </div>\n'
            f'</details>'
        )

    text = re.sub(r'<details(?:\s+[^>]*)?>(.*?)</details>', repl_details, text, flags=re.DOTALL | re.IGNORECASE)

    # 3. Tables
    def repl_table(m):
        table_str = m.group(0).strip()
        lines = [l.strip() for l in table_str.splitlines() if l.strip()]
        if len(lines) < 2:
            return table_str

        header_cols = [c.strip() for c in lines[0].split('|')[1:-1]]
        # line 1 is separator |---|---|
        body_rows = lines[2:]

        out = ['<div class="table-wrapper"><table class="md-table">']
        out.append('  <thead><tr>')
        for h in header_cols:
            out.append(f'    <th>{inline_markdown(h)}</th>')
        out.append('  </tr></thead>')
        out.append('  <tbody>')
        for r in body_rows:
            cols = [c.strip() for c in r.split('|')[1:-1]]
            out.append('    <tr>')
            for c in cols:
                out.append(f'      <td>{inline_markdown(c)}</td>')
            out.append('    </tr>')
        out.append('  </tbody></table></div>')
        return '\n'.join(out)

    table_pattern = re.compile(r'((?:^[ \t]*\|[^\n]+\|[ \t]*\n)+)', re.MULTILINE)
    text = table_pattern.sub(repl_table, text)

    # 4. Headers (##, ###, ####)
    def repl_h4(m):
        title = m.group(1).strip()
        return f'<h4 class="md-h4">{inline_markdown(title)}</h4>'
    def repl_h3(m):
        title = m.group(1).strip()
        hid = slugify(title)
        return f'<h3 class="md-h3" id="{hid}">{inline_markdown(title)}</h3>'
    def repl_h2(m):
        title = m.group(1).strip()
        hid = slugify(title)
        return f'<h2 class="md-h2" id="{hid}">{inline_markdown(title)}</h2>'
    def repl_h1(m):
        title = m.group(1).strip()
        hid = slugify(title)
        return f'<h1 class="md-h1" id="{hid}">{inline_markdown(title)}</h1>'

    text = re.sub(r'^####\s+(.+)$', repl_h4, text, flags=re.MULTILINE)
    text = re.sub(r'^###\s+(.+)$', repl_h3, text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.+)$', repl_h2, text, flags=re.MULTILINE)
    text = re.sub(r'^#\s+(.+)$', repl_h1, text, flags=re.MULTILINE)

    # 5. Blockquotes (> ...)
    def repl_quote(m):
        quote_text = m.group(1).strip()
        lines = [re.sub(r'^[ \t]*>[ \t]?', '', l) for l in quote_text.splitlines()]
        inner_rendered = inline_markdown('\n'.join(lines))
        return f'<blockquote class="md-blockquote">{inner_rendered}</blockquote>'

    text = re.sub(r'((?:^[ \t]*>[^\n]*\n?)+)', repl_quote, text, flags=re.MULTILINE)

    # 6. Unordered lists
    def repl_ul(m):
        items = m.group(0).strip().splitlines()
        lis = []
        for it in items:
            it_clean = re.sub(r'^[ \t]*[-*]\s+', '', it)
            lis.append(f'  <li>{inline_markdown(it_clean)}</li>')
        return '<ul class="md-ul">\n' + '\n'.join(lis) + '\n</ul>'

    text = re.sub(r'((?:^[ \t]*[-*]\s+[^\n]+\n?)+)', repl_ul, text, flags=re.MULTILINE)

    # 7. Ordered lists
    def repl_ol(m):
        items = m.group(0).strip().splitlines()
        lis = []
        for it in items:
            it_clean = re.sub(r'^[ \t]*\d+\.\s+', '', it)
            lis.append(f'  <li>{inline_markdown(it_clean)}</li>')
        return '<ol class="md-ol">\n' + '\n'.join(lis) + '\n</ol>'

    text = re.sub(r'((?:^[ \t]*\d+\.\s+[^\n]+\n?)+)', repl_ol, text, flags=re.MULTILINE)

    # 8. Horizontal rules
    text = re.sub(r'^[ \t]*---[ \t]*$', '<hr class="md-hr">', text, flags=re.MULTILINE)

    # 9. Paragraphs
    paragraphs = []
    for chunk in text.split('\n\n'):
        chunk = chunk.strip()
        if not chunk:
            continue
        if any(chunk.startswith(prefix) for prefix in [
            '<h1', '<h2', '<h3', '<h4', '<div', '<blockquote', '<ul', '<ol', '<hr', '<details',
            '___MERMAID_PLACEHOLDER_', '___CODE_PLACEHOLDER_'
        ]):
            paragraphs.append(chunk)
        else:
            paragraphs.append(f'<p class="md-p">{inline_markdown(chunk)}</p>')
    text = '\n\n'.join(paragraphs)

    # 10. Restore code blocks
    for i, cb in enumerate(code_blocks):
        text = text.replace(f"___CODE_PLACEHOLDER_{i}___", cb)

    # 11. Restore mermaid blocks into Canvas Containers (1:1 DSA standard)
    for i, (diag_id, code) in enumerate(mermaid_blocks):
        escaped_mermaid = html.escape(code.strip())
        wb = (
            f'<div class="canvas-container" id="canvas-{diag_id}">\n'
            f'  <div class="canvas-header-bar">\n'
            f'    <span class="canvas-type-tag">📐 Architecture Blueprint · State Machine</span>\n'
            f'    <div class="canvas-controls-group">\n'
            f'      <button class="canvas-tool-btn zoom-out-btn" title="Zoom Out">−</button>\n'
            f'      <span class="zoom-level-badge">100%</span>\n'
            f'      <button class="canvas-tool-btn zoom-in-btn" title="Zoom In">+</button>\n'
            f'      <button class="canvas-tool-btn zoom-reset-btn" title="Reset Zoom">⟲</button>\n'
            f'      <button class="canvas-tool-btn fullscreen-btn" title="View Fullscreen Theater">⛶</button>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'  <div class="canvas-viewport">\n'
            f'    <div class="canvas-content-surface">\n'
            f'      <pre class="mermaid" id="{diag_id}">\n{escaped_mermaid}\n      </pre>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'  <div class="canvas-caption">Architecture &amp; structural interaction graph</div>\n'
            f'</div>'
        )
        text = text.replace(f"___MERMAID_PLACEHOLDER_{i}___", wb)

    return text

def inline_markdown(text: str) -> str:
    """Format inline markdown: bold, italic, code, links, strikethrough."""
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code class="inline-code">\1</code>', text)
    # Bold italic
    text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
    # Strikethrough
    text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)

    # Links: [text](href)
    def repl_link(m):
        ltxt = m.group(1)
        lhref = m.group(2).strip()

        # Check if internal chapter directory link e.g. ./01%20-%20Singleton%20%28Creational%29/
        # or ./24%20-%20Unit%20of%20Work%20%28Architectural%29/
        unquoted = urllib.parse.unquote(lhref)
        # Extract folder match
        dir_match = re.search(r'(\d{2})\s*-\s*([^(/\\]+)', unquoted)
        if dir_match:
            num = dir_match.group(1)
            name = slugify(dir_match.group(2).strip())
            return f'<a href="#chapter-{num}-{name}" class="md-link">{ltxt}</a>'

        if lhref.startswith('http://') or lhref.startswith('https://'):
            return f'<a href="{lhref}" target="_blank" rel="noopener noreferrer" class="md-link md-link-ext">{ltxt}</a>'
        return f'<a href="{lhref}" class="md-link">{ltxt}</a>'

    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl_link, text)
    return text

def parse_python_example(py_path: Path) -> dict:
    """Extract metadata, scenario, key insight, and code from a Python example file."""
    code_text = py_path.read_text(encoding="utf-8", errors="ignore")
    lines = code_text.splitlines()

    title = py_path.stem.replace("example_", "").replace("_", " ").title()
    framework = "Pure Python"
    scenario = ""
    key_insight = ""

    # Parse header docstring if present
    doc_match = re.search(r'^\s*"""(.*?)"""', code_text, flags=re.DOTALL)
    if doc_match:
        doc = doc_match.group(1)
        # Extract Example: Title
        m_title = re.search(r'Example:\s*([^\n]+)', doc, re.IGNORECASE)
        if m_title:
            title = m_title.group(1).strip()
        # Extract Framework:
        m_fw = re.search(r'Framework:\s*([^\n]+)', doc, re.IGNORECASE)
        if m_fw:
            framework = m_fw.group(1).strip()
        # Extract Real-World Scenario
        m_scen = re.search(r'REAL-WORLD SCENARIO:\s*-+\s*([^\n]+(?:\n[^\n]+)*?)(?=\n[A-Z\s-]+:|\Z)', doc, re.IGNORECASE)
        if m_scen:
            scenario = " ".join(l.strip() for l in m_scen.group(1).strip().splitlines() if l.strip())
        # Extract Key Insight
        m_ins = re.search(r'KEY INSIGHT:\s*-+\s*([^\n]+(?:\n[^\n]+)*?)(?=\n[A-Z\s-]+:|\Z)', doc, re.IGNORECASE)
        if m_ins:
            key_insight = " ".join(l.strip() for l in m_ins.group(1).strip().splitlines() if l.strip())

    line_count = len(lines)
    escaped_code = html.escape(code_text.rstrip())

    # Framework badge styling
    fw_lower = framework.lower()
    badge_cls = "dna-label-code"
    if "django" in fw_lower:
        badge_cls = "dna-label-django"
    elif "fastapi" in fw_lower:
        badge_cls = "dna-label-fastapi"
    elif "sqlalchemy" in fw_lower:
        badge_cls = "dna-label-sqlalchemy"
    elif "celery" in fw_lower:
        badge_cls = "dna-label-celery"

    return {
        "filename": py_path.name,
        "title": title,
        "framework": framework,
        "scenario": scenario,
        "key_insight": key_insight,
        "line_count": line_count,
        "escaped_code": escaped_code,
        "badge_cls": badge_cls,
    }

def main():
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║  📚 Compiling Design Patterns Living Documentation Portal       ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    # Discover all numbered chapter folders
    folders = sorted([
        d for d in ROOT_DIR.iterdir()
        if d.is_dir() and re.match(r'^\d{2}\s*-', d.name)
    ], key=lambda d: d.name)

    print(f"→ Discovered {len(folders)} pattern chapter directories.")

    SITE_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)

    manifest_patterns = []
    manifest_examples = []
    chapters_html = []
    sidebar_items_html = []

    total_examples = 0
    total_diagrams = 0

    for idx, f_path in enumerate(folders):
        folder_name = f_path.name
        slug = get_chapter_slug(folder_name)
        tier = get_tier_for_folder(folder_name)
        tier_data = TIERS[tier]

        # Extract number, clean title, and suffix label
        # E.g. "01 - Singleton (Creational)" -> num="01", raw_title="Singleton", suffix_label="Creational"
        # "00 - Foundations" -> num="00", raw_title="Foundations", suffix_label="Foundations"
        # "27 - Patterns in the Wild (Capstone)" -> num="27", raw_title="Patterns in the Wild", suffix_label="Capstone"
        m_info = re.match(r'^(\d{2})\s*-\s*([^(]+?)(?:\s*\(([^)]+)\))?$', folder_name)
        if m_info:
            num = m_info.group(1).strip()
            raw_title = m_info.group(2).strip()
            suffix_label = m_info.group(3).strip() if m_info.group(3) else tier
        else:
            num = f"{idx:02d}"
            raw_title = folder_name
            suffix_label = tier

        print(f"  [{num}] Compiling {raw_title} ({tier} - {suffix_label})...")

        # 1. Read theory.md
        theory_file = f_path / "theory.md"
        theory_content = ""
        gof_intent = ""
        summary_5yo = ""
        if theory_file.exists():
            theory_content = theory_file.read_text(encoding="utf-8", errors="ignore")
            # Extract 5yo explanation
            m_5yo = re.search(r'## 🧒 The 5-Year-Old Explanation\s*\n+([^\n#]+)', theory_content)
            if m_5yo:
                summary_5yo = m_5yo.group(1).strip()
            # Extract GoF Intent
            m_gof = re.search(r'### Intent \(GoF\)\s*\n+>\s*([^\n]+)', theory_content)
            if m_gof:
                gof_intent = m_gof.group(1).strip()

        rendered_theory = render_markdown(theory_content, folder_name)

        # 2. Discover and parse Python example files
        py_files = sorted(f_path.glob("*.py"))
        examples_data = []
        for py_f in py_files:
            ex = parse_python_example(py_f)
            examples_data.append(ex)
            total_examples += 1

            manifest_examples.append({
                "slug": f"{slug}-{slugify(ex['filename'])}",
                "chapter_slug": slug,
                "chapter_num": num,
                "chapter_title": raw_title,
                "tier": tier,
                "filename": ex["filename"],
                "title": ex["title"],
                "framework": ex["framework"],
                "scenario": ex["scenario"],
                "key_insight": ex["key_insight"],
                "lines": ex["line_count"],
            })

        # Render examples HTML
        examples_html_parts = []
        if examples_data:
            examples_html_parts.append(
                f'<div class="chapter-examples-section">\n'
                f'  <h3 class="section-subheading">⚡ Interactive Python 3.14 Implementations ({len(examples_data)})</h3>'
            )
            for ex in examples_data:
                ex_id = f"example-{slug}-{slugify(ex['filename'])}"
                meta_block = ""
                scenario_html = f'<div class="meta-scenario"><strong>Scenario:</strong> {ex["scenario"]}</div>' if ex["scenario"] else ""
                insight_html = f'<div class="meta-insight"><strong>Key Insight:</strong> {ex["key_insight"]}</div>' if ex["key_insight"] else ""
                if scenario_html or insight_html:
                    meta_block = f'    <div class="example-meta-bar">\n      {scenario_html}\n      {insight_html}\n    </div>\n'

                examples_html_parts.append(
                    f'  <div class="example-card" id="{ex_id}">\n'
                    f'    <div class="example-card-header">\n'
                    f'      <div class="example-title-cluster">\n'
                    f'        <span class="example-filename">{ex["filename"]}</span>\n'
                    f'        <span class="example-title">{ex["title"]}</span>\n'
                    f'      </div>\n'
                    f'      <div class="example-meta-cluster">\n'
                    f'        <span class="dna-label {ex["badge_cls"]}">{ex["framework"]}</span>\n'
                    f'        <span class="example-lines">{ex["line_count"]} lines</span>\n'
                    f'        <button class="copy-btn" title="Copy clean Python code">Copy</button>\n'
                    f'      </div>\n'
                    f'    </div>\n'
                    f'{meta_block}'
                    f'    <div class="code-container">\n'
                    f'      <pre><code class="language-python">{ex["escaped_code"]}</code></pre>\n'
                    f'    </div>\n'
                    f'  </div>\n'
                )
            examples_html_parts.append('</div>')
        rendered_examples = "\n".join(examples_html_parts)

        # Build chapter card (1:1 DSA standard)
        tier_class = tier.lower()
        chapter_card = (
            f'<section class="pattern-chapter is-collapsed" id="{slug}" data-tier="{tier}">\n'
            f'  <div class="chapter-header-bar" data-target="#{slug}">\n'
            f'    <div class="chapter-header-left">\n'
            f'      <span class="chapter-chevron">▶</span>\n'
            f'      <span class="tree-icon" style="font-size:1.3rem;">{tier_data["icon"]}</span>\n'
            f'      <h2 class="chapter-title">{num} · {html.escape(raw_title)}</h2>\n'
            f'    </div>\n'
            f'    <div class="chapter-header-right">\n'
            f'      <span class="hero-tag tag-{tier_class}">{html.escape(suffix_label)}</span>\n'
            f'      <button class="chapter-toggle-btn">Expand</button>\n'
            f'    </div>\n'
            f'  </div>\n'
            f'  <div class="chapter-content-body">\n'
            f'    <div class="chapter-theory-content">\n'
            f'{rendered_theory}\n'
            f'    </div>\n'
            f'{rendered_examples}\n'
            f'  </div>\n'
            f'</section>'
        )
        chapters_html.append(chapter_card)

        # Build sidebar navigation tree group (1:1 DSA standard with expandable tree children)
        prob_links = []
        prob_links.append(f'<a href="#{slug}" class="nav-tree-link" style="color:var(--accent-cyan);font-weight:600;">📖 Pattern Anatomy &amp; Theory</a>')
        for ex in examples_data:
            ex_id = f"example-{slug}-{slugify(ex['filename'])}"
            prob_links.append(f'<a href="#{ex_id}" class="nav-tree-link">⚡ {html.escape(ex["title"])}</a>')

        sidebar_items_html.append(f'''
        <div class="nav-tree-group" id="nav-group-{slug}" data-tier="{tier}">
          <div class="nav-tree-header" data-target="#{slug}">
            <div class="tree-title-group">
              <span class="tree-chevron">▶</span>
              <span class="tree-icon">{tier_data["icon"]}</span>
              <span class="tree-title-text">{num} · {html.escape(raw_title)}</span>
            </div>
            <span class="nav-pill pill-{tier_class}">{html.escape(suffix_label)}</span>
          </div>
          <div class="nav-tree-children">
            {''.join(prob_links)}
          </div>
        </div>
        ''')

        manifest_patterns.append({
            "num": num,
            "slug": slug,
            "title": raw_title,
            "tier": tier,
            "folder": folder_name,
            "gof_intent": gof_intent,
            "summary_5yo": summary_5yo,
            "example_count": len(examples_data),
        })

    # Save manifest.json
    manifest = {
        "version": "2.0.0",
        "generated_at": "2026-11-03",
        "tiers": TIERS,
        "patterns": manifest_patterns,
        "examples": manifest_examples,
        "stats": {
            "patterns_count": len(manifest_patterns),
            "examples_count": total_examples,
            "diagrams_count": _DIAGRAM_COUNTER,
        }
    }
    with open(CATALOG_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"✅ Generated manifest.json ({len(manifest_patterns)} patterns, {total_examples} examples, {_DIAGRAM_COUNTER} diagrams).")

    # Read shell index template from docs/site/index.html
    template_path = DOCS_SITE_DIR / "index.html"
    if not template_path.exists():
        print(f"❌ Error: {template_path} not found.")
        sys.exit(1)

    template_html = template_path.read_text(encoding="utf-8")

    # Inject generated content
    hydrated_html = template_html.replace(
        "<!-- CHAPTERS_INJECTION_POINT -->",
        "\n".join(chapters_html)
    ).replace(
        "<!-- SIDEBAR_NAV_INJECTION_POINT -->",
        "\n".join(sidebar_items_html)
    ).replace(
        "{{PATTERNS_COUNT}}", str(len(manifest_patterns))
    ).replace(
        "{{EXAMPLES_COUNT}}", str(total_examples)
    ).replace(
        "{{DIAGRAMS_COUNT}}", str(_DIAGRAM_COUNTER)
    )

    with open(SITE_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(hydrated_html)

    # Copy style.css, app.js, and any assets
    if (DOCS_SITE_DIR / "style.css").exists():
        shutil.copy(DOCS_SITE_DIR / "style.css", SITE_DIR / "style.css")
    if (DOCS_SITE_DIR / "app.js").exists():
        shutil.copy(DOCS_SITE_DIR / "app.js", SITE_DIR / "app.js")
    if (DOCS_SITE_DIR / "assets").exists():
        shutil.copytree(DOCS_SITE_DIR / "assets", SITE_DIR / "assets", dirs_exist_ok=True)

    print(f"🎉 Build complete: Static bundle written to {SITE_DIR}/")

if __name__ == "__main__":
    main()

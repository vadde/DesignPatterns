---
name: design-patterns-docs-portal
description: >-
  Authoritative engineering guide and automated testing protocol for the Design Patterns Living Documentation Portal (https://vadde.github.io/DesignPatterns/). Covers Year 2500 cosmic liquid-glass design system, Aero Mica ambient halos, draggable sidebar resizer invariants, commute gadget mobile drawer, zero-truncation titles, touch-overflow containment, 1:1 ScrollSpy sync, Mermaid SVG layout rules, Safari WebKit flex sizing, sub-millisecond Theater mode workbench, KaTeX math typesetting, interactive Pattern Finder & Decision Matrix, Cmd+K fuzzy search, Unicode monospace box-drawing alignment engine, and the 15-gate automated headless audit suite.
---

# 🏛️ Design Patterns Living Documentation Portal Engineering Skill

This skill is the **authoritative engineering protocol and single source of truth** for maintaining, styling, extending, and verifying the `vadde/DesignPatterns` Living Documentation Portal ([https://vadde.github.io/DesignPatterns/](https://vadde.github.io/DesignPatterns/)).

AI coding assistants and engineers must follow this guide whenever adding patterns, modifying CSS styles, rendering architecture diagrams, building interactive widgets, or testing on mobile and desktop viewports.

---

## 🏛️ Portal Architecture & File Map

The documentation portal is built with **zero build toolchain dependencies** (pure vanilla HTML5, CSS3, ES2022 JavaScript, and standard CDN libraries):

```
DesignPatterns/
├── Makefile                                       # Canonical DevEx commands (docs-build, docs-serve, docs-test, etc.)
├── specs/
│   └── SPEC-001-design-patterns-futuristic-docs-portal.md # Ratified PRD & System Architecture Spec
├── docs/site/
│   ├── index.html                                 # Hydrated Year 2500 Command Deck Shell
│   ├── style.css                                  # Liquid glass tokens, Aero Mica halos, resizer, responsive layout
│   └── app.js                                     # ScrollSpy, resizer, mobile drawer, search modal, lazy renderers
├── scripts/
│   ├── build-docs.py                              # Production catalog compiler (28 chapters, 38 python examples)
│   ├── build-docs.sh                              # Static bundle packaging script (outputs to _site/)
│   ├── test-docs.sh                               # 15-Gate automated headless verification suite
│   ├── audit_ascii_boxes.py                       # Unicode UAX #11 monospace box-drawing linter and formatter
│   ├── audit_collapsible_elements.py              # Collapsible details & raw HTML block auditor
│   ├── audit_links_and_anchors.py                 # Universal link & local path leak prevention auditor
│   └── audit_monospace_badging.py                 # Monospace semantic badge and tree auditor
├── .agents/skills/design-patterns-docs-portal/
│   └── SKILL.md                                   # YOU ARE HERE — Authoritative design & engineering protocol
└── .github/workflows/
    ├── ci.yml                                     # Parallel CI verification (Python compile, Ruff, 15-Gate Audit)
    └── docs-publish.yml                           # CD workflow deploying verified main pushes to GitHub Pages
```

---

## 🎨 Design System & Multi-Theme Engine

The portal uses a **deep cosmic liquid-glass design system with Aero Mica ambient halos** supporting 4 distinct themes:

### Color Palette Tokens

| Token | CSS Variable | Hex / RGBA Value | Purpose |
|---|---|---|---|
| **Canvas Deep Base** | `--bg-deep` | `#050813` | Deep space background canvas |
| **Card Surface** | `--bg-card` | `rgba(13, 20, 39, 0.65)` | Glassmorphism card background |
| **Card Border** | `--bg-card-border` | `rgba(255, 255, 255, 0.08)` | Subtle translucent glass card edge |
| **Hover Border** | `--bg-card-border-glow` | `rgba(0, 242, 254, 0.35)` | Interactive element border focus |
| **Cyan Accent** | `--accent-cyan` | `#00f2fe` | Primary interactive focus, active items, Creational badges |
| **Violet Accent** | `--accent-violet` | `#a855f7` | Diagram relational links, Structural badges |
| **Emerald Accent** | `--accent-emerald` | `#10b981` | Behavioral badges, Foundations status |
| **Amber Accent** | `--accent-amber` | `#f59e0b` | Architectural badges, caution callouts |
| **Rose Accent** | `--accent-rose` | `#f43f5e` | Capstone alerts, Anti-patterns |
| **Primary Text** | `--text-main` | `#f1f5f9` | High-contrast body text and titles |
| **Muted Text** | `--text-muted` | `#94a3b8` | Subtitles, parameter descriptions |
| **Dim Text** | `--text-dim` | `#64748b` | Captions, footnotes, table metadata |

### Theme Invariants:
1. **Liquid Glass (`[data-theme="liquid"]`)**: Default deep cosmic glass with vibrant cyan/violet edge glows.
2. **Aero Mica (`[data-theme="mica"]`)**:
   - **High-Contrast Code Blocks**: Code blocks MUST use dark text on bright frosted surface (`background: rgba(255, 255, 255, 0.95); color: #0f172a !important;`). Never leave white-on-white text!
   - **Frosted Theater Tool Buttons**: Must use high-contrast frosted pills (`background: rgba(255, 255, 255, 0.22); border: 1px solid rgba(255, 255, 255, 0.55); color: #ffffff !important;`) so that `+`, `−`, `100%`, and `Fit` buttons pop over the dark modal header.
3. **Obsidian Dark (`[data-theme="matrix"]` or `[data-theme="obsidian"]`)**: Matte pure-black stealth palette with neon emerald accents.
4. **Cyberpunk Neon (`[data-theme="holo"]` or `[data-theme="cyberpunk"]`)**: High-saturation electric cyan and amber contrast grid.

---

## ↔️ Interactive Draggable Sidebar Resizer & Collapsible Rail Standard

The navigation sidebar supports continuous draggable resizing and full collapsible rail distraction-free mode:

### Operational Invariants:
1. **Collapsible Distraction-Free Reading**:
   - Closed via `#sidebar-close-btn` inside sidebar or `#sidebar-dock-toggle` in header.
   - When collapsed, `body.sidebar-collapsed` shifts `.sidebar` by `margin-left: calc(-1 * var(--sidebar-width)); opacity: 0; visibility: hidden;` and hides `.sidebar-resizer`.
   - Floating reopen tab `#floating-sidebar-toggle` appears on the left edge (`top: calc(var(--topbar-height) + 14px); left: 14px;`).
   - Global keyboard shortcuts: `⌘B`, `Ctrl+B`, or `[` (when not focused in inputs) toggle the rail instantly.
   - State persisted in `localStorage.setItem('dp_sidebar_collapsed', 'true' / 'false')`.
2. **Bounds Clamping**: Resizing strictly clamped between `MIN_WIDTH = 240px` and `MAX_WIDTH = 560px`.
3. **Dragging Performance**: During drag, `body.resizing-sidebar` sets `cursor: col-resize !important; user-select: none !important;`.
4. **Persistence**: Width choice is saved to `localStorage.setItem('dp_sidebar_width', width)`.
5. **Double-Click Reset**: Double-clicking resets `--sidebar-width` to default `330px`.
6. **Zero-Truncation Invariant**: Never clip navigation titles with single-line ellipses (`white-space: normal; word-break: break-word`).

---

## 📱 Commute Gadget Mobile Navigation Architecture

1. On viewports $\le 1024\text{px}$, sidebar transitions into an off-canvas slide-out drawer (`width: min(86vw, 360px)`).
2. **Stacking Context Invariant**: `#mobile-drawer-backdrop` (`z-index: 1100`) must be placed inside `.layout-container` right before `.sidebar` (`z-index: 1200`).
3. **Sticky Scroll Invariant**: **Never use `overflow-x: hidden` on `html` or `body`**. Always use `overflow-x: clip;` to prevent breaking `position: sticky`.
4. Wrap all `<table>` elements in `<div class="table-wrapper">` with horizontal touch scrolling and explicit min-width (`min-width: 520px`).

---

## 🎯 Universal Delegated In-Page Navigation

All in-page anchors (`a[href^="#"]`) use delegated event interception in `app.js`:
1. Intercepts click and cancels native jump.
2. Checks if target element or any ancestor is collapsed (`.pattern-chapter.is-collapsed` or closed `<details>`).
3. Automatically uncollapses containing chapters, opens `<details>`, and updates toggle buttons.
4. Forces synchronous layout flush (`targetEl.getBoundingClientRect()`).
5. Smoothly scrolls with exact 72px cushion:
   ```javascript
   const y = targetEl.getBoundingClientRect().top + window.pageYOffset - 72;
   window.scrollTo({ top: y, behavior: 'smooth' });
   ```
6. Applies a temporary flash focus highlight (`flash-focus`) for 1800ms. Zero treasure hunting!

---

## ⚡ Sub-10ms "Expand All" SLA

When opening all 28 chapters simultaneously:
- **Root-Cause Pitfall**: Synchronous execution of diagram render calls inside accordion `toggle` events freezes the CPU for seconds.
- **The Protocol**: Guard accordion `toggle` listeners with `STATE.isBatchExpanding`:
  ```javascript
  STATE.isBatchExpanding = true;
  document.querySelectorAll('.pattern-chapter').forEach(c => c.classList.remove('is-collapsed'));
  document.querySelectorAll('.theory-details, .example-card').forEach(d => { d.open = true; });
  setTimeout(() => {
    STATE.isBatchExpanding = false;
    renderVisibleDiagrams();
  }, 50);
  ```

---

## 📊 Mermaid Diagram & Safari WebKit Layout Rules

### 1. Isolated `mermaid.render()` Execution:
Never rely on uncoordinated `mermaid.run()`. Always use isolated, direct rendering:
```javascript
const { svg, bindFunctions } = await window.mermaid.render(renderId, code);
el.innerHTML = svg;
if (bindFunctions) bindFunctions(el);
```

### 2. The Safari WebKit Flex-SVG Sizing Invariant:
- **Never use `width: auto !important` on `.mermaid svg`** inside flex containers. In WebKit/Safari, an SVG with percentage width and `width: auto` collapses to `0px × 0px`!
- **CSS Rule**:
  ```css
  .mermaid svg {
    display: block !important;
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    max-height: 580px !important;
    object-fit: contain;
    margin: 0 auto;
  }
  ```
- **Intrinsic Dimension Injection**:
  Extract `vbW` and `vbH` from the SVG's `viewBox` and inject explicit W3C attributes:
  ```javascript
  svgEl.setAttribute('width', vbW);
  svgEl.setAttribute('height', vbH);
  svgEl.style.aspectRatio = `${vbW} / ${vbH}`;
  ```

### 3. Escaping & Syntax Cleanliness:
- Escape `<` and `>` in node labels as `&lt;` / `&gt;` or `≤` / `≥`.
- Every diagram MUST have a globally unique `id="mermaid-diagram-{uid}"`.

---

## 🔍 Fullscreen Theater Mode Workbench

Implemented using native HTML5 `<dialog id="theater-modal">`:

### Critical Invariants:
1. **Sub-Millisecond Zoom/Pan SLA**:
   - `.theater-content-surface` MUST specify `transition: none !important;`.
   - Caching `cachedVbW` and `cachedVbH` upon open eliminates forced reflows during zoom.
2. **Clear UX Distinction: `100%` vs `Fit`**:
   - `100%` (`theaterZoomReset`): Resets scale to **`1.0`** (1:1 native pixel scale).
   - `Fit` (`theaterZoomFit`): Dynamically calculates exact scale based on live viewport boundaries and SVG `viewBox` (`scale = Math.min(availW / vbW, availH / vbH)`).
3. **Anti-Dismissal Rule (No Accidental Close)**:
   - Clicks or drag-releases on `.theater-viewport` or SVG canvas MUST NEVER close the modal!
   - **Only** the explicit Close button (`✕`) or the `Escape` key closes the theater.
4. **Diagram Text Selection**:
   - `.theater-content-surface svg text, foreignObject, span` must have `user-select: text !important; cursor: text;`.
5. **Exact Scroll Position Restoration**:
   - Save `scrollY` before modal open and restore on close.

---

## 🔊 Curated Web Audio Haptic System (`HapticAudio`)

Tactile acoustic feedback synthesized purely via Web Audio API oscillators:

| Interaction | Waveform | Frequency Ramp | Duration | Sensation |
|---|---|---|---|---|
| **Expand Chapter** | Sine | 540Hz → 880Hz | 38ms | Mechanical switch opening |
| **Collapse Chapter** | Sine | 780Hz → 420Hz | 38ms | Snappy latch folding |
| **Sidebar Drag / Toggle**| Triangle | 440Hz → 760Hz | 50ms | Smooth sliding panel reveal |
| **Copy Code** | Arpeggiated Sine | C6 (1046Hz) + E6 (1318Hz) | 90ms | Celebratory success chime |
| **Theme Change** | Triangle | 600Hz → 1200Hz | 60ms | Cosmic palette shift |
| **Theater Launch** | Harmonic Sine | 440Hz → 880Hz | 70ms | Cinematic workbench focus |
| **Search Open (⌘K)** | High-transient Sine | 1180Hz → 1480Hz | 40ms | Holographic HUD ping |

---

## 🧪 15-Gate Headless Automated Verification Suite

Run before every commit or push:
```bash
make docs-test
```

1. **Core Assets Presence**: `index.html`, `style.css`, `app.js`, `catalog/manifest.json`.
2. **Catalog Completeness & Search Index**: 28 chapters, 38 Python code implementations indexed.
3. **Mermaid Label Escaping**: No unescaped `<` or `>` inside node labels.
4. **CSS SVG Sizing Invariants**: No `width: auto !important` on `.mermaid svg`.
5. **KaTeX Integration**: Delimiters, styles, and auto-render execution.
6. **Draggable Sidebar Resizer**: Bounds clamping, `col-resize`, and `localStorage` persistence.
7. **Mobile Drawer & Anti-Clobbering**: Sticky-safe `overflow-x: clip;` and z-index hierarchy.
8. **Table & Touch Containment**: `.table-wrapper` with touch scrolling and `min-width: 520px`.
9. **Relative Path Invariants**: All asset links use relative addressing (`./`) for `/DesignPatterns/` GitHub Pages.
10. **Static Bundle Footprint**: Bundle size strictly $<25\text{MB}$.
11. **Mermaid ID Uniqueness & Clean Navigation**: 84+ unique IDs, isolated rendering, zero legacy footer links.
12. **Unicode Monospace Box-Drawing Alignment**: 100% of ASCII and Unicode box tables and cards aligned.
13. **Collapsible Details & Zero Raw HTML Block Escaping**: 100% semantic `<details>` with valid summary and body.
14. **Monospace Semantic Badging**: Framework and pattern badges valid and rendered.
15. **Hyperlink Integrity & Local Path Prevention**: Zero `file://` or `/Users/` paths; zero raw `.md` or `.py` file links; zero external GitHub jumps for internal files; 100% internal fragment anchor resolution.

---

## 🛠️ Canonical Developer Commands

| Command | Purpose |
|---|---|
| `make help` | Interactive targets menu |
| `make docs-build` | Compiles 28 chapters and generates hydrated static site in `_site/` |
| `make docs-serve` | Serves documentation locally on `http://localhost:4000/` |
| `make docs-test` | Runs the full 15-gate headless verification suite |
| `make test-boxes` | Audits ASCII and Unicode box-drawing alignment |
| `make format-boxes` | Realigns and formats all ASCII/Unicode boxes across the repository in place |
| `make test` | Runs AST syntax compilation across all 38 Python implementations |
| `make lint` | Runs Ruff linter + box alignment check |
| `make ci` | Runs full CI audit suite locally (test + lint + docs-test) |
| `make clean` | Cleans `_site/` and pycache artifacts |

/**
 * ==============================================================================
 * vadde/DesignPatterns — Year 2500 Command Deck Runtime (ES2022)
 * Pure vanilla JavaScript with zero third-party framework runtime weight.
 * Features:
 *   - Directional Web Audio API Haptic Acoustic Engine (HapticAudio)
 *   - 4-Theme Engine (Liquid Glass, Aero Mica, Holo 2050, Matrix Obsidian)
 *   - Draggable Sidebar Resizer Standard (240px - 560px with double-click reset)
 *   - Distraction-Free Collapsible Reading Rail (⌘B / [)
 *   - Commute Gadget Mobile Navigation Drawer
 *   - Sub-Millisecond Theater Mode Workbench (Zoom In/Out, 100%, Fit, Panning)
 *   - Universal Delegated In-Page Navigation & Flash-Focus Pulse
 *   - Sub-10ms Expand All SLA with isBatchExpanding Guard
 *   - Global Fuzzy Search Modal HUD (⌘K)
 *   - Interactive Pattern Finder & Decision Matrix
 * ==============================================================================
 */

(function () {
  'use strict';

  // Global UI State
  const STATE = {
    theme: localStorage.getItem('dp_theme') || 'liquid',
    sidebarWidth: parseInt(localStorage.getItem('dp_sidebar_width'), 10) || 330,
    isSidebarCollapsed: localStorage.getItem('dp_sidebar_collapsed') === 'true',
    audioEnabled: localStorage.getItem('dp_audio_enabled') !== 'false',
    isFocusMode: true,
    isProgrammaticScroll: false,
    programmaticScrollTimer: null,
    isBatchExpanding: false,
    manifest: null,
    renderedDiagrams: new Set(),
    theater: {
      activeDiagramId: null,
      scale: 1.0,
      panX: 0,
      panY: 0,
      isPanning: false,
      startX: 0,
      startY: 0,
      cachedVbW: 800,
      cachedVbH: 600,
      savedScrollY: 0
    }
  };

  // ---------------------------------------------------------------------------
  // 1. DIRECTIONAL WEB AUDIO API HAPTIC ENGINE (HapticAudio)
  // ---------------------------------------------------------------------------
  const HapticAudio = {
    ctx: null,

    getContext() {
      if (!this.ctx) {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (AudioCtx) {
          this.ctx = new AudioCtx();
        }
      }
      if (this.ctx && this.ctx.state === 'suspended') {
        this.ctx.resume();
      }
      return this.ctx;
    },

    canPlay() {
      return STATE.audioEnabled && !STATE.isBatchExpanding;
    },

    _lastAudioTime: 0,
    throttle(intervalMs = 18) {
      const now = performance.now();
      if (now - this._lastAudioTime < intervalMs) return true;
      this._lastAudioTime = now;
      return false;
    },

    tap() {
      if (!this.canPlay() || this.throttle(18)) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(920, now);
        osc.frequency.exponentialRampToValueAtTime(560, now + 0.022);
        gain.gain.setValueAtTime(0.038, now);
        gain.gain.exponentialRampToValueAtTime(0.0005, now + 0.022);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.025);
      } catch (e) {}
    },

    sidebarOpen() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(760, now + 0.055);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.0005, now + 0.055);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.06);
      } catch (e) {}
    },

    sidebarClose() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(680, now);
        osc.frequency.exponentialRampToValueAtTime(320, now + 0.045);
        gain.gain.setValueAtTime(0.045, now);
        gain.gain.exponentialRampToValueAtTime(0.0005, now + 0.045);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.05);
      } catch (e) {}
    },

    // 1. Expand Chapter
    expand() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(540, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.038);
        gain.gain.setValueAtTime(0.06, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.038);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.038);
      } catch (e) {}
    },

    // 2. Collapse Chapter
    collapse() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(780, now);
        osc.frequency.exponentialRampToValueAtTime(420, now + 0.038);
        gain.gain.setValueAtTime(0.05, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.038);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.038);
      } catch (e) {}
    },

    // 3. Sidebar Rail Slide
    sidebarToggle() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(760, now + 0.05);
        gain.gain.setValueAtTime(0.07, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.05);
      } catch (e) {}
    },

    // 4. Celebratory Code Copy Chime (C6 + E6)
    copySuccess() {
      if (!STATE.audioEnabled) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        [1046.50, 1318.51].forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          const start = now + idx * 0.04;
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, start);
          gain.gain.setValueAtTime(0.07, start);
          gain.gain.exponentialRampToValueAtTime(0.001, start + 0.09);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(start);
          osc.stop(start + 0.09);
        });
      } catch (e) {}
    },

    // 5. Theme Palette Shift
    themeChange() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(600, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.06);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.06);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.06);
      } catch (e) {}
    },

    // 6. Theater Launch
    theaterOpen() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.07);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.07);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.07);
      } catch (e) {}
    },

    // 7. Search HUD Ping
    searchOpen() {
      if (!this.canPlay()) return;
      try {
        const ctx = this.getContext();
        if (!ctx) return;
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1180, now);
        osc.frequency.exponentialRampToValueAtTime(1480, now + 0.04);
        gain.gain.setValueAtTime(0.06, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.04);
      } catch (e) {}
    }
  };

  // ---------------------------------------------------------------------------
  // 2. THEME ENGINE
  // ---------------------------------------------------------------------------
  function initThemeEngine() {
    applyTheme(STATE.theme);

    document.querySelectorAll('.theme-pill-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        applyTheme(btn.dataset.themeSet);
        HapticAudio.themeChange();
      });
    });

    document.addEventListener('keydown', e => {
      if (e.key.toLowerCase() === 't' && !isInputFocused(e)) {
        e.preventDefault();
        const themes = ['liquid', 'mica', 'holo', 'matrix'];
        const currentIdx = themes.indexOf(STATE.theme);
        const nextTheme = themes[(currentIdx + 1) % themes.length];
        applyTheme(nextTheme);
        HapticAudio.themeChange();
      }
    });
  }

  function applyTheme(themeName) {
    STATE.theme = themeName;
    document.documentElement.setAttribute('data-theme', themeName);
    localStorage.setItem('dp_theme', themeName);

    document.querySelectorAll('.theme-pill-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.themeSet === themeName);
    });
  }

  // ---------------------------------------------------------------------------
  // 3. AMBIENT HALO ENGINE
  // ---------------------------------------------------------------------------
  function initHaloEngine() {
    const orb = document.getElementById('halo-orb');
    if (!orb) return;

    window.addEventListener('pointermove', e => {
      document.documentElement.style.setProperty('--mx', `${e.clientX}px`);
      document.documentElement.style.setProperty('--my', `${e.clientY}px`);
    }, { passive: true });
  }

  // ---------------------------------------------------------------------------
  // 4. INTERACTIVE DRAGGABLE SIDEBAR RESIZER STANDARD
  // ---------------------------------------------------------------------------
  function initSidebarResizer() {
    const resizer = document.getElementById('sidebar-resizer');
    const sidebar = document.getElementById('main-sidebar');
    if (!resizer || !sidebar) return;

    const MIN_WIDTH = 240;
    const MAX_WIDTH = 560;
    const DEFAULT_WIDTH = 330;

    // Apply saved width
    const savedWidth = Math.min(Math.max(STATE.sidebarWidth, MIN_WIDTH), MAX_WIDTH);
    document.documentElement.style.setProperty('--sidebar-width', `${savedWidth}px`);

    let isDragging = false;

    resizer.addEventListener('mousedown', e => {
      if (e.button !== 0) return;
      isDragging = true;
      document.body.classList.add('resizing-sidebar');
      e.preventDefault();
    });

    window.addEventListener('mousemove', e => {
      if (!isDragging) return;
      const newWidth = Math.min(Math.max(e.clientX, MIN_WIDTH), MAX_WIDTH);
      document.documentElement.style.setProperty('--sidebar-width', `${newWidth}px`);
      STATE.sidebarWidth = newWidth;
    });

    window.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        document.body.classList.remove('resizing-sidebar');
        localStorage.setItem('dp_sidebar_width', STATE.sidebarWidth);
      }
    });

    // Double-click reset to default width
    resizer.addEventListener('dblclick', () => {
      document.documentElement.style.setProperty('--sidebar-width', `${DEFAULT_WIDTH}px`);
      STATE.sidebarWidth = DEFAULT_WIDTH;
      localStorage.setItem('dp_sidebar_width', DEFAULT_WIDTH);
      HapticAudio.sidebarToggle();
    });
  }

  // ---------------------------------------------------------------------------
  // 5. COLLAPSIBLE SIDEBAR RAIL (⌘B / [)
  // ---------------------------------------------------------------------------
  function initDesktopSidebarToggle() {
    const dockBtn = document.getElementById('sidebar-dock-toggle');
    const closeBtn = document.getElementById('sidebar-close-btn');
    const floatBtn = document.getElementById('floating-sidebar-toggle');

    if (STATE.isSidebarCollapsed) {
      document.body.classList.add('sidebar-collapsed');
    }

    function toggleRail() {
      const isCollapsed = document.body.classList.toggle('sidebar-collapsed');
      STATE.isSidebarCollapsed = isCollapsed;
      localStorage.setItem('dp_sidebar_collapsed', isCollapsed ? 'true' : 'false');
      HapticAudio.sidebarToggle();
    }

    if (dockBtn) dockBtn.addEventListener('click', toggleRail);
    if (closeBtn) closeBtn.addEventListener('click', toggleRail);
    if (floatBtn) floatBtn.addEventListener('click', toggleRail);

    document.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'b') {
        e.preventDefault();
        toggleRail();
      } else if (e.key === '[' && !isInputFocused(e)) {
        e.preventDefault();
        toggleRail();
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 6. COMMUTE GADGET MOBILE DRAWER
  // ---------------------------------------------------------------------------
  function initMobileDrawer() {
    const toggleBtn = document.getElementById('mobile-nav-toggle');
    const backdrop = document.getElementById('mobile-drawer-backdrop');
    if (!toggleBtn || !backdrop) return;

    toggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('mobile-drawer-open');
      HapticAudio.sidebarToggle();
    });

    backdrop.addEventListener('click', () => {
      document.body.classList.remove('mobile-drawer-open');
      HapticAudio.sidebarToggle();
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 1024 && document.body.classList.contains('mobile-drawer-open')) {
        document.body.classList.remove('mobile-drawer-open');
      }
    }, { passive: true });
  }

  // ---------------------------------------------------------------------------
  // 7. PRECISION NAVIGATION & CHAPTER EXPANSION
  // ---------------------------------------------------------------------------
  function triggerDiagramRenders(container) {
    if (STATE.isBatchExpanding) return;
    setTimeout(() => {
      renderVisibleDiagrams(container);
    }, 16);
  }

  function ensureChapterExpanded(targetEl, shouldScroll = false) {
    if (!targetEl) return;
    if (shouldScroll) {
      navigateToTarget(targetEl);
      return;
    }
    const chapter = targetEl.closest('.pattern-chapter');
    if (chapter) {
      chapter.classList.remove('is-collapsed');
      const toggleBtn = chapter.querySelector('.chapter-toggle-btn');
      if (toggleBtn) toggleBtn.innerText = 'Collapse';
      triggerDiagramRenders(chapter);
    }
    if (targetEl.tagName === 'DETAILS') {
      targetEl.open = true;
      triggerDiagramRenders(targetEl);
    } else {
      const parentDetails = targetEl.closest('details');
      if (parentDetails) {
        parentDetails.open = true;
        triggerDiagramRenders(parentDetails);
      }
    }
  }

  function navigateToTarget(targetEl) {
    if (!targetEl) return;

    STATE.isProgrammaticScroll = true;
    clearTimeout(STATE.programmaticScrollTimer);

    // 1. Uncollapse the containing chapter
    const chapter = targetEl.closest('.pattern-chapter') || (targetEl.classList.contains('pattern-chapter') ? targetEl : null);
    if (chapter) {
      if (STATE.isFocusMode) {
        document.querySelectorAll('.pattern-chapter').forEach(c => {
          if (c !== chapter) {
            c.classList.add('is-collapsed');
            const btn = c.querySelector('.chapter-toggle-btn');
            if (btn) btn.innerText = 'Expand';
          }
        });
      }
      chapter.classList.remove('is-collapsed');
      const toggleBtn = chapter.querySelector('.chapter-toggle-btn');
      if (toggleBtn) toggleBtn.innerText = 'Collapse';

      // Synchronize Left Navigation tree
      const targetId = chapter.id;
      const sidebarGroup = document.getElementById(`nav-group-${targetId}`);
      if (sidebarGroup) {
        document.querySelectorAll('.nav-tree-group').forEach(g => {
          if (g === sidebarGroup) {
            g.classList.add('expanded');
          } else if (STATE.isFocusMode) {
            g.classList.remove('expanded');
          }
        });
        document.querySelectorAll('.nav-tree-header').forEach(h => {
          const g = h.closest('.nav-tree-group');
          if (g === sidebarGroup) {
            h.classList.add('active-branch');
          } else {
            h.classList.remove('active-branch');
          }
        });
        sidebarGroup.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }

      triggerDiagramRenders(chapter);
    }

    // 2. If target is inside a <details>, open it!
    if (targetEl.tagName === 'DETAILS') {
      targetEl.open = true;
      triggerDiagramRenders(targetEl);
    } else {
      const parentDetails = targetEl.closest('details');
      if (parentDetails) {
        parentDetails.open = true;
        triggerDiagramRenders(parentDetails);
      }
    }

    // Highlight active link in sidebar
    document.querySelectorAll('.nav-tree-link').forEach(link => {
      const href = link.getAttribute('href');
      if (href === `#${targetEl.id}` || (chapter && href === `#${chapter.id}`)) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });

    // 3. Force synchronous layout reflow so the browser finalizes all coordinates
    void document.body.offsetHeight;

    // 4. Calculate offset with 72px cushion
    const rect = targetEl.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const targetY = rect.top + scrollTop - 72;

    window.scrollTo({
      top: Math.max(0, targetY),
      behavior: 'smooth'
    });

    // 5. Flash-focus pulse animation
    targetEl.classList.remove('flash-focus');
    void targetEl.offsetWidth;
    targetEl.classList.add('flash-focus');
    setTimeout(() => targetEl.classList.remove('flash-focus'), 1800);

    // 6. Close mobile drawer if open
    if (window.innerWidth <= 1024 && document.body.classList.contains('mobile-drawer-open')) {
      document.body.classList.remove('mobile-drawer-open');
    }

    // Reset programmatic scroll guard after scrolling finishes
    STATE.programmaticScrollTimer = setTimeout(() => {
      STATE.isProgrammaticScroll = false;
    }, 800);
  }

  function handleInitialDeepLink() {
    const hash = window.location.hash;
    if (hash && hash.length > 1) {
      try {
        const targetEl = document.querySelector(hash);
        if (targetEl) {
          ensureChapterExpanded(targetEl, true);
          return;
        }
      } catch (e) {}
    }
  }

  // ---------------------------------------------------------------------------
  // 8. CHAPTER ACCORDIONS, FOCUS MODE & BATCH EXPAND SLA
  // ---------------------------------------------------------------------------
  function initCollapsibleChapters() {
    const expandAllBtn = document.getElementById('btn-expand-all') || document.getElementById('expand-all-btn');
    const collapseAllBtn = document.getElementById('btn-collapse-all') || document.getElementById('collapse-all-btn');
    const focusModeBtn = document.getElementById('btn-focus-mode');
    const sidebarExpandBtn = document.getElementById('sidebar-expand-all');
    const sidebarCollapseBtn = document.getElementById('sidebar-collapse-all');

    function setActiveReadingBtn(btn) {
      [expandAllBtn, focusModeBtn, collapseAllBtn].forEach(b => {
        if (b) b.classList.remove('active');
      });
      if (btn) btn.classList.add('active');
    }

    // Click handler for Chapter Header Bar
    document.querySelectorAll('.chapter-header-bar, .chapter-card-header').forEach(header => {
      header.addEventListener('click', (e) => {
        // Ignore clicks on inner copy buttons or links
        if (e.target.closest('.copy-btn, a')) return;

        const chapter = header.closest('.pattern-chapter');
        if (!chapter) return;

        const isCollapsed = chapter.classList.contains('is-collapsed');
        if (isCollapsed) {
          // Expanding
          if (STATE.isFocusMode) {
            document.querySelectorAll('.pattern-chapter').forEach(c => {
              if (c !== chapter) {
                c.classList.add('is-collapsed');
                const btn = c.querySelector('.chapter-toggle-btn');
                if (btn) btn.innerText = 'Expand';
              }
            });
          }
          chapter.classList.remove('is-collapsed');
          const toggleBtn = chapter.querySelector('.chapter-toggle-btn');
          if (toggleBtn) toggleBtn.innerText = 'Collapse';

          // Sync with sidebar tree
          const targetId = chapter.id;
          const sidebarGroup = document.getElementById(`nav-group-${targetId}`);
          if (sidebarGroup) {
            if (STATE.isFocusMode) {
              document.querySelectorAll('.nav-tree-group').forEach(g => {
                if (g !== sidebarGroup) g.classList.remove('expanded');
              });
            }
            sidebarGroup.classList.add('expanded');
          }

          triggerDiagramRenders(chapter);
          HapticAudio.expand();
        } else {
          // Collapsing
          chapter.classList.add('is-collapsed');
          const toggleBtn = chapter.querySelector('.chapter-toggle-btn');
          if (toggleBtn) toggleBtn.innerText = 'Expand';
          HapticAudio.collapse();
        }
      });
    });

    // Expand All Chapters & Details
    if (expandAllBtn) {
      expandAllBtn.addEventListener('click', () => {
        STATE.isFocusMode = false;
        STATE.isBatchExpanding = true;
        setActiveReadingBtn(expandAllBtn);
        document.querySelectorAll('.pattern-chapter').forEach(c => {
          c.classList.remove('is-collapsed');
          const btn = c.querySelector('.chapter-toggle-btn');
          if (btn) btn.innerText = 'Collapse';
        });
        document.querySelectorAll('.problem-card, .theory-details, .md-details').forEach(d => {
          d.open = true;
        });
        setTimeout(() => {
          STATE.isBatchExpanding = false;
          renderVisibleDiagrams();
        }, 50);
        HapticAudio.expand();
      });
    }

    // Collapse All Chapters & Details
    if (collapseAllBtn) {
      collapseAllBtn.addEventListener('click', () => {
        STATE.isFocusMode = false;
        setActiveReadingBtn(collapseAllBtn);
        document.querySelectorAll('.pattern-chapter').forEach(c => {
          c.classList.add('is-collapsed');
          const btn = c.querySelector('.chapter-toggle-btn');
          if (btn) btn.innerText = 'Expand';
        });
        document.querySelectorAll('.problem-card, .md-details').forEach(d => {
          d.open = false;
        });
        document.querySelectorAll('.nav-tree-group').forEach(g => g.classList.remove('expanded'));
        document.querySelectorAll('.nav-tree-header').forEach(h => h.classList.remove('active-branch'));
        document.querySelectorAll('.nav-tree-link').forEach(l => l.classList.remove('active'));
        HapticAudio.collapse();
      });
    }

    // Focus Mode Toggle / Activate
    if (focusModeBtn) {
      focusModeBtn.addEventListener('click', () => {
        STATE.isFocusMode = true;
        setActiveReadingBtn(focusModeBtn);
        // Collapse all except first open chapter
        const chapters = Array.from(document.querySelectorAll('.pattern-chapter'));
        let foundOpen = false;
        chapters.forEach(c => {
          if (!foundOpen && !c.classList.contains('is-collapsed')) {
            foundOpen = true;
          } else {
            c.classList.add('is-collapsed');
            const btn = c.querySelector('.chapter-toggle-btn');
            if (btn) btn.innerText = 'Expand';
          }
        });
        if (!foundOpen && chapters.length > 0) {
          chapters[0].classList.remove('is-collapsed');
          const btn = chapters[0].querySelector('.chapter-toggle-btn');
          if (btn) btn.innerText = 'Collapse';
          triggerDiagramRenders(chapters[0]);
        }
        HapticAudio.tap();
      });
    }

    // Sidebar Expand / Collapse All
    if (sidebarExpandBtn) {
      sidebarExpandBtn.addEventListener('click', () => {
        document.querySelectorAll('.nav-tree-group').forEach(g => g.classList.add('expanded'));
        HapticAudio.expand();
      });
    }

    if (sidebarCollapseBtn) {
      sidebarCollapseBtn.addEventListener('click', () => {
        document.querySelectorAll('.nav-tree-group').forEach(g => g.classList.remove('expanded'));
        HapticAudio.collapse();
      });
    }

    // Main content: Markdown Details clicks for audio consistency
    document.addEventListener('click', e => {
      const summary = e.target.closest('.md-summary, summary');
      if (!summary) return;
      const details = summary.closest('details');
      if (!details || STATE.isBatchExpanding) return;

      if (details.open) {
        HapticAudio.collapse();
      } else {
        HapticAudio.expand();
      }
    });

    // Handle deep links on load
    handleInitialDeepLink();
  }

  // ---------------------------------------------------------------------------
  // 9. SIDEBAR TREE NAVIGATION & FILTER ENGINE
  // ---------------------------------------------------------------------------
  function initSidebarFilters() {
    const filterInput = document.getElementById('sidebar-filter-input');
    const treeGroups = document.querySelectorAll('.nav-tree-group');
    const tierChips = document.querySelectorAll('.tier-chip');

    let activeTier = 'all';

    function applyFilters() {
      const query = filterInput ? filterInput.value.trim().toLowerCase() : '';
      treeGroups.forEach(group => {
        const titleEl = group.querySelector('.tree-title-text');
        const titleText = titleEl ? titleEl.innerText.toLowerCase() : '';
        const tier = group.dataset.tier || '';

        const matchesQuery = !query || titleText.includes(query);
        const matchesTier = activeTier === 'all' || tier === activeTier;

        if (matchesQuery && matchesTier) {
          group.style.display = '';
        } else {
          group.style.display = 'none';
        }
      });
    }

    if (filterInput) {
      filterInput.addEventListener('input', applyFilters);
    }

    tierChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const t = chip.dataset.tierFilter;
        tierChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        activeTier = t;
        applyFilters();
        HapticAudio.tap();
      });
    });

    // Clicking group headers in sidebar
    document.querySelectorAll('.nav-tree-header').forEach(header => {
      header.addEventListener('click', () => {
        const group = header.closest('.nav-tree-group');
        if (!group) return;
        const willExpand = !group.classList.contains('expanded');

        if (STATE.isFocusMode && willExpand) {
          document.querySelectorAll('.nav-tree-group').forEach(g => {
            if (g !== group) g.classList.remove('expanded');
          });
        }
        group.classList.toggle('expanded', willExpand);

        // Bi-directional synchrony: expand corresponding chapter in content!
        const targetId = header.getAttribute('data-target');
        if (targetId) {
          const targetSection = document.querySelector(targetId);
          if (targetSection && willExpand) {
            ensureChapterExpanded(targetSection, true);
          }
        }
        if (willExpand) {
          HapticAudio.expand();
        } else {
          HapticAudio.collapse();
        }
      });
    });

    // Universal precision navigation for in-page anchors across the entire portal
    document.addEventListener('click', e => {
      const link = e.target.closest('a[href^="#"]');
      if (!link) return;
      const href = link.getAttribute('href');
      if (href && href !== '#' && href.length > 1) {
        const targetEl = document.querySelector(href);
        if (targetEl) {
          e.preventDefault();
          navigateToTarget(targetEl);
          if (history.pushState) {
            history.pushState(null, null, href);
          }
          HapticAudio.tap();
        }
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 10. SCROLLSPY
  // ---------------------------------------------------------------------------
  function initScrollSpy() {
    const chapters = Array.from(document.querySelectorAll('.pattern-chapter'));
    const navLinks = Array.from(document.querySelectorAll('.nav-tree-link'));
    const navGroups = Array.from(document.querySelectorAll('.nav-tree-group'));
    const navHeaders = Array.from(document.querySelectorAll('.nav-tree-header'));
    if (!chapters.length) return;

    let currentActiveChapterId = null;
    let ticking = false;

    function onScrollUpdate() {
      ticking = false;
      if (STATE.isProgrammaticScroll) return;

      const scrollY = window.scrollY || window.pageYOffset;
      const headerHeight = 72; // 64px header + 8px cushion

      // If at top of page, clear active classes
      if (scrollY < 220) {
        if (currentActiveChapterId !== null) {
          currentActiveChapterId = null;
          navGroups.forEach(g => g.classList.remove('expanded'));
          navHeaders.forEach(h => h.classList.remove('active-branch'));
          navLinks.forEach(l => l.classList.remove('active'));
        }
        return;
      }

      // Find the chapter currently active on screen
      let activeChapter = null;
      for (let i = chapters.length - 1; i >= 0; i--) {
        const ch = chapters[i];
        const rect = ch.getBoundingClientRect();
        if (rect.top <= headerHeight + 60) {
          activeChapter = ch;
          break;
        }
      }
      if (!activeChapter && chapters.length > 0) {
        activeChapter = chapters[0];
      }

      if (activeChapter && activeChapter.id !== currentActiveChapterId) {
        currentActiveChapterId = activeChapter.id;
        const targetGroup = document.getElementById(`nav-group-${currentActiveChapterId}`);

        navGroups.forEach(g => {
          if (g === targetGroup) {
            g.classList.add('expanded');
          } else if (STATE.isFocusMode) {
            g.classList.remove('expanded');
          }
        });

        navHeaders.forEach(h => {
          const g = h.closest('.nav-tree-group');
          h.classList.toggle('active-branch', g === targetGroup);
        });

        navLinks.forEach(l => {
          const href = l.getAttribute('href');
          l.classList.toggle('active', href === `#${currentActiveChapterId}`);
        });

        if (targetGroup) {
          targetGroup.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
      }
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(onScrollUpdate);
        ticking = true;
      }
    }, { passive: true });
  }

  // ---------------------------------------------------------------------------
  // 10. LAZY MERMAID RENDERING & FULLSCREEN THEATER WORKBENCH
  // ---------------------------------------------------------------------------
  async function renderVisibleDiagrams(scope = document) {
    if (!window.mermaid) return;

    const mermaidPres = scope.querySelectorAll('pre.mermaid:not([data-processed="true"])');
    for (const pre of mermaidPres) {
      const id = pre.id;
      if (!id || STATE.renderedDiagrams.has(id)) continue;

      const code = pre.textContent.trim();
      try {
        const renderId = `svg-${id}`;
        const { svg, bindFunctions } = await window.mermaid.render(renderId, code);
        pre.innerHTML = svg;
        pre.setAttribute('data-processed', 'true');
        STATE.renderedDiagrams.add(id);

        if (bindFunctions) bindFunctions(pre);

        // Safari WebKit sizing invariant injection
        const svgEl = pre.querySelector('svg');
        if (svgEl) {
          const viewBox = svgEl.getAttribute('viewBox');
          if (viewBox) {
            const parts = viewBox.split(/[\s,]+/).map(Number);
            if (parts.length === 4) {
              const vbW = parts[2];
              const vbH = parts[3];
              svgEl.setAttribute('width', vbW);
              svgEl.setAttribute('height', vbH);
              svgEl.style.aspectRatio = `${vbW} / ${vbH}`;
            }
          }
        }
      } catch (err) {
        console.warn(`Mermaid render failed for ${id}:`, err);
      }
    }
  }

  function initTheaterWorkbench() {
    const modal = document.getElementById('theater-modal');
    const surface = document.getElementById('theater-content-surface');
    const titleEl = document.getElementById('theater-diagram-title');
    const zoomBadge = document.getElementById('theater-zoom-badge');
    const closeBtn = document.getElementById('theater-close-btn');
    const zoomInBtn = document.getElementById('theater-zoom-in');
    const zoomOutBtn = document.getElementById('theater-zoom-out');
    const zoomResetBtn = document.getElementById('theater-zoom-reset');
    const zoomFitBtn = document.getElementById('theater-zoom-fit');
    const viewport = document.getElementById('theater-viewport');

    if (!modal || !surface) return;

    // Launch theater on button click
    document.addEventListener('click', async e => {
      const launchBtn = e.target.closest('.theater-launch-btn');
      if (!launchBtn) return;

      const targetId = launchBtn.dataset.target;
      const sourcePre = document.getElementById(targetId);
      if (!sourcePre) return;

      // Ensure diagram is rendered
      if (!sourcePre.hasAttribute('data-processed')) {
        await renderVisibleDiagrams(sourcePre.parentElement);
      }

      const svgEl = sourcePre.querySelector('svg');
      if (!svgEl) return;

      STATE.theater.savedScrollY = window.pageYOffset;
      STATE.theater.activeDiagramId = targetId;

      // Cache dimensions from viewBox
      const vb = svgEl.getAttribute('viewBox');
      if (vb) {
        const parts = vb.split(/[\s,]+/).map(Number);
        if (parts.length === 4) {
          STATE.theater.cachedVbW = parts[2];
          STATE.theater.cachedVbH = parts[3];
        }
      }

      // Clone SVG into theater surface
      surface.innerHTML = svgEl.outerHTML;
      if (titleEl) {
        const chapter = sourcePre.closest('.pattern-chapter');
        const chapterTitle = chapter ? chapter.querySelector('.chapter-title').textContent : 'Master Relationships';
        titleEl.textContent = `Architecture Workbench: ${chapterTitle}`;
      }

      modal.showModal();
      HapticAudio.theaterOpen();
      applyTheaterFit();
    });

    // Close Theater
    function closeTheater() {
      if (!modal.open) return;
      modal.close();
      surface.innerHTML = '';
      window.scrollTo({ top: STATE.theater.savedScrollY, behavior: 'instant' });
      HapticAudio.collapse();

      // Pulse focus back to source diagram
      if (STATE.theater.activeDiagramId) {
        const source = document.getElementById(STATE.theater.activeDiagramId);
        if (source) {
          const card = source.closest('.mermaid-workbench, .hero-diagram-card');
          if (card) {
            card.classList.add('flash-focus');
            setTimeout(() => card.classList.remove('flash-focus'), 1800);
          }
        }
      }
    }

    if (closeBtn) closeBtn.addEventListener('click', closeTheater);

    // ANTI-DISMISSAL RULE:
    // Clicks on the viewport or dialog backdrop do NOT close the modal.
    // Only the explicit close button or Escape key closes the theater workbench.
    modal.addEventListener('cancel', e => {
      e.preventDefault();
      closeTheater();
    });

    // Sub-millisecond Zoom controls
    function updateTransform() {
      surface.style.transform = `translate(${STATE.theater.panX}px, ${STATE.theater.panY}px) scale(${STATE.theater.scale})`;
      if (zoomBadge) {
        zoomBadge.textContent = `${Math.round(STATE.theater.scale * 100)}%`;
      }
    }

    function applyTheaterFit() {
      const availW = viewport.clientWidth - 60;
      const availH = viewport.clientHeight - 60;
      const fitScale = Math.min(availW / STATE.theater.cachedVbW, availH / STATE.theater.cachedVbH, 2.5);
      STATE.theater.scale = Math.max(fitScale, 0.2);
      STATE.theater.panX = 0;
      STATE.theater.panY = 0;
      updateTransform();
    }

    if (zoomInBtn) {
      zoomInBtn.addEventListener('click', () => {
        STATE.theater.scale = Math.min(STATE.theater.scale * 1.25, 4.0);
        updateTransform();
      });
    }
    if (zoomOutBtn) {
      zoomOutBtn.addEventListener('click', () => {
        STATE.theater.scale = Math.max(STATE.theater.scale / 1.25, 0.25);
        updateTransform();
      });
    }
    if (zoomResetBtn) {
      zoomResetBtn.addEventListener('click', () => {
        STATE.theater.scale = 1.0;
        STATE.theater.panX = 0;
        STATE.theater.panY = 0;
        updateTransform();
      });
    }
    if (zoomFitBtn) {
      zoomFitBtn.addEventListener('click', applyTheaterFit);
    }

    // Panning within viewport
    viewport.addEventListener('pointerdown', e => {
      // Don't pan if selecting text
      if (e.target.closest('text, span, foreignObject')) return;
      STATE.theater.isPanning = true;
      STATE.theater.startX = e.clientX - STATE.theater.panX;
      STATE.theater.startY = e.clientY - STATE.theater.panY;
      viewport.setPointerCapture(e.pointerId);
    });

    viewport.addEventListener('pointermove', e => {
      if (!STATE.theater.isPanning) return;
      STATE.theater.panX = e.clientX - STATE.theater.startX;
      STATE.theater.panY = e.clientY - STATE.theater.startY;
      updateTransform();
    });

    viewport.addEventListener('pointerup', e => {
      if (STATE.theater.isPanning) {
        STATE.theater.isPanning = false;
        viewport.releasePointerCapture(e.pointerId);
      }
    });

    // Mouse wheel zoom
    viewport.addEventListener('wheel', e => {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 1.15 : 0.85;
      STATE.theater.scale = Math.min(Math.max(STATE.theater.scale * delta, 0.2), 4.0);
      updateTransform();
    }, { passive: false });
  }

  // ---------------------------------------------------------------------------
  // 11. ONE-CLICK CODE COPY
  // ---------------------------------------------------------------------------
  function initCopyButtons() {
    document.addEventListener('click', async e => {
      const copyBtn = e.target.closest('.copy-btn');
      if (!copyBtn) return;

      const container = copyBtn.closest('.code-container, .example-card');
      if (!container) return;

      const codeEl = container.querySelector('code');
      if (!codeEl) return;

      try {
        await navigator.clipboard.writeText(codeEl.textContent);
        copyBtn.textContent = 'Copied!';
        copyBtn.classList.add('copied');
        HapticAudio.copySuccess();

        setTimeout(() => {
          copyBtn.textContent = 'Copy';
          copyBtn.classList.remove('copied');
        }, 2000);
      } catch (err) {
        console.error('Copy failed:', err);
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 12. GLOBAL FUZZY SEARCH MODAL HUD (⌘K)
  // ---------------------------------------------------------------------------
  async function initSearchHUD() {
    const triggerBtn = document.getElementById('hud-search-trigger');
    const modal = document.getElementById('search-modal');
    const input = document.getElementById('search-dialog-input');
    const resultsContainer = document.getElementById('search-results-list');
    const filterPills = document.querySelectorAll('.search-pill');

    if (!modal || !input) return;

    // Load manifest if not loaded
    async function ensureManifest() {
      if (STATE.manifest) return STATE.manifest;
      try {
        const res = await fetch('./catalog/manifest.json');
        STATE.manifest = await res.json();
      } catch (err) {
        console.warn('Could not load catalog manifest:', err);
      }
      return STATE.manifest;
    }

    function openSearch() {
      ensureManifest();
      modal.showModal();
      input.value = '';
      input.focus();
      HapticAudio.searchOpen();
      renderSearchResults('');
    }

    function closeSearch() {
      if (modal.open) {
        modal.close();
      }
    }

    if (triggerBtn) triggerBtn.addEventListener('click', openSearch);

    modal.addEventListener('click', e => {
      if (e.target === modal) closeSearch();
    });

    document.addEventListener('keydown', e => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (modal.open) closeSearch();
        else openSearch();
      }
    });

    let currentFilter = 'all';
    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        currentFilter = pill.dataset.searchFilter;
        renderSearchResults(input.value);
      });
    });

    input.addEventListener('input', () => {
      renderSearchResults(input.value);
    });

    function renderSearchResults(query) {
      if (!STATE.manifest) return;
      const q = query.toLowerCase().trim();
      if (!q) {
        resultsContainer.innerHTML = '<div class="search-empty-state">Type a pattern name, framework (FastAPI, Django, SQLAlchemy), or intent...</div>';
        return;
      }

      const matches = [];

      // Search patterns
      STATE.manifest.patterns.forEach(p => {
        if (currentFilter !== 'all' && p.tier !== currentFilter) return;
        const score = (
          (p.title.toLowerCase().includes(q) ? 10 : 0) +
          (p.num.includes(q) ? 10 : 0) +
          (p.gof_intent && p.gof_intent.toLowerCase().includes(q) ? 5 : 0) +
          (p.summary_5yo && p.summary_5yo.toLowerCase().includes(q) ? 3 : 0)
        );
        if (score > 0) {
          matches.push({
            type: 'Pattern',
            title: `${p.num} - ${p.title}`,
            href: `#${p.slug}`,
            badge: p.tier,
            snippet: p.gof_intent || p.summary_5yo,
            score
          });
        }
      });

      // Search examples / code
      STATE.manifest.examples.forEach(ex => {
        if (currentFilter !== 'all' && ex.tier !== currentFilter) return;
        const score = (
          (ex.title.toLowerCase().includes(q) ? 8 : 0) +
          (ex.framework.toLowerCase().includes(q) ? 6 : 0) +
          (ex.filename.toLowerCase().includes(q) ? 5 : 0) +
          (ex.scenario && ex.scenario.toLowerCase().includes(q) ? 4 : 0) +
          (ex.key_insight && ex.key_insight.toLowerCase().includes(q) ? 4 : 0)
        );
        if (score > 0) {
          matches.push({
            type: 'Implementation',
            title: `${ex.chapter_num} ${ex.chapter_title}: ${ex.title}`,
            href: `#example-${ex.chapter_slug}-${ex.filename.replace(/\.py$/, '')}`,
            badge: ex.framework,
            snippet: ex.scenario || ex.key_insight || `${ex.lines} lines of runnable Python code`,
            score
          });
        }
      });

      matches.sort((a, b) => b.score - a.score);

      if (!matches.length) {
        resultsContainer.innerHTML = `<div class="search-empty-state">No matching patterns or code found for "${q}".</div>`;
        return;
      }

      resultsContainer.innerHTML = matches.slice(0, 15).map(m => `
        <a href="${m.href}" class="search-result-item" onclick="document.getElementById('search-modal').close()">
          <div class="search-result-top">
            <span class="search-result-title">${m.title}</span>
            <span class="search-result-badge">${m.badge}</span>
          </div>
          <div class="search-result-snippet">${m.snippet || ''}</div>
        </a>
      `).join('');
    }
  }

  // ---------------------------------------------------------------------------
  // 13. INTERACTIVE PATTERN FINDER & DECISION MATRIX
  // ---------------------------------------------------------------------------
  async function initDecisionMatrix() {
    const toggleBtn = document.getElementById('quick-finder-toggle-btn');
    const hud = document.getElementById('pattern-finder-hud');
    const closeBtn = document.getElementById('finder-close-btn');
    const grid = document.getElementById('finder-matrix-grid');
    const frameworkPills = document.querySelectorAll('.framework-pill');

    if (!toggleBtn || !hud || !grid) return;

    const MATRIX_DATA = [
      { problem: "Need exactly one instance globally (config, DB connection pool)", pattern: "01 Singleton", slug: "chapter-01-singleton", tier: "Creational", fw: ["pure python", "django"] },
      { problem: "Create objects without specifying exact concrete class", pattern: "02 Factory Method", slug: "chapter-02-factory-method", tier: "Creational", fw: ["pure python", "fastapi"] },
      { problem: "Create matching families of related or dependent objects", pattern: "03 Abstract Factory", slug: "chapter-03-abstract-factory", tier: "Creational", fw: ["pure python", "sqlalchemy"] },
      { problem: "Construct complex objects step-by-step with fluent API", pattern: "04 Builder", slug: "chapter-04-builder", tier: "Creational", fw: ["pure python"] },
      { problem: "Clone existing objects instead of creating from scratch", pattern: "05 Prototype", slug: "chapter-05-prototype", tier: "Creational", fw: ["pure python"] },
      { problem: "Make incompatible interfaces work together smoothly", pattern: "06 Adapter", slug: "chapter-06-adapter", tier: "Structural", fw: ["pure python"] },
      { problem: "Vary abstraction AND implementation independently", pattern: "07 Bridge", slug: "chapter-07-bridge", tier: "Structural", fw: ["pure python"] },
      { problem: "Treat individual objects and tree compositions uniformly", pattern: "08 Composite", slug: "chapter-08-composite", tier: "Structural", fw: ["pure python"] },
      { problem: "Add behavior to objects dynamically without subclassing", pattern: "09 Decorator", slug: "chapter-09-decorator", tier: "Structural", fw: ["pure python", "fastapi"] },
      { problem: "Simplify a complex subsystem with a clean high-level facade", pattern: "10 Facade", slug: "chapter-10-facade", tier: "Structural", fw: ["pure python"] },
      { problem: "Share immutable state to support vast numbers of fine objects", pattern: "11 Flyweight", slug: "chapter-11-flyweight", tier: "Structural", fw: ["pure python"] },
      { problem: "Control, cache, or lazily protect access to an object", pattern: "12 Proxy", slug: "chapter-12-proxy", tier: "Structural", fw: ["pure python", "django"] },
      { problem: "Pass a request along an extensible chain of handlers", pattern: "13 Chain of Resp.", slug: "chapter-13-chain-of-responsibility", tier: "Behavioral", fw: ["pure python", "fastapi"] },
      { problem: "Encapsulate a request as an object (undo, queue, redo)", pattern: "14 Command", slug: "chapter-14-command", tier: "Behavioral", fw: ["pure python", "celery"] },
      { problem: "Access elements sequentially without exposing collection internals", pattern: "15 Iterator", slug: "chapter-15-iterator", tier: "Behavioral", fw: ["pure python"] },
      { problem: "Reduce chaotic many-to-many dependencies between objects", pattern: "16 Mediator", slug: "chapter-16-mediator", tier: "Behavioral", fw: ["pure python"] },
      { problem: "Save and restore object state snapshots without breaking encapsulation", pattern: "17 Memento", slug: "chapter-17-memento", tier: "Behavioral", fw: ["pure python"] },
      { problem: "Notify multiple objects about state changes automatically", pattern: "18 Observer", slug: "chapter-18-observer", tier: "Behavioral", fw: ["pure python", "celery"] },
      { problem: "Alter object behavior dynamically when its internal state changes", pattern: "19 State", slug: "chapter-19-state", tier: "Behavioral", fw: ["pure python"] },
      { problem: "Swap interchangeable algorithms or policies at runtime", pattern: "20 Strategy", slug: "chapter-20-strategy", tier: "Behavioral", fw: ["pure python", "fastapi"] },
      { problem: "Define algorithm skeleton in base class; let subclasses customize steps", pattern: "21 Template Method", slug: "chapter-21-template-method", tier: "Behavioral", fw: ["pure python", "django"] },
      { problem: "Add operations to complex object structures without modifying them", pattern: "22 Visitor", slug: "chapter-22-visitor", tier: "Behavioral", fw: ["pure python"] },
      { problem: "Abstract data persistence layer behind collection-like domain interface", pattern: "23 Repository Pattern", slug: "chapter-23-repository-pattern", tier: "Architectural", fw: ["sqlalchemy", "fastapi"] },
      { problem: "Coordinate business transactions and commit atomic changes across repos", pattern: "24 Unit of Work", slug: "chapter-24-unit-of-work", tier: "Architectural", fw: ["sqlalchemy"] },
      { problem: "Decouple dependency creation from dependency consumption", pattern: "25 Dependency Injection", slug: "chapter-25-dependency-injection", tier: "Architectural", fw: ["fastapi", "pure python"] },
      { problem: "Track domain state changes as an immutable append-only event log", pattern: "26 Event Sourcing & CQRS", slug: "chapter-26-event-sourcing-cqrs", tier: "Architectural", fw: ["pure python", "celery"] }
    ];

    function renderMatrix(fwFilter = 'all') {
      const filtered = MATRIX_DATA.filter(item => {
        if (fwFilter === 'all') return true;
        return item.fw.includes(fwFilter);
      });

      grid.innerHTML = filtered.map(item => `
        <a href="#${item.slug}" class="finder-card">
          <div class="finder-card-header">
            <span class="finder-card-title">${item.pattern}</span>
            <span class="finder-card-tier">${item.tier}</span>
          </div>
          <div class="finder-card-problem">${item.problem}</div>
        </a>
      `).join('');
    }

    renderMatrix('all');

    toggleBtn.addEventListener('click', () => {
      const isVisible = hud.style.display !== 'none';
      hud.style.display = isVisible ? 'none' : 'block';
      HapticAudio.themeChange();
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        hud.style.display = 'none';
        HapticAudio.collapse();
      });
    }

    frameworkPills.forEach(pill => {
      pill.addEventListener('click', () => {
        frameworkPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        renderMatrix(pill.dataset.framework);
        HapticAudio.sidebarToggle();
      });
    });

    document.addEventListener('keydown', e => {
      if (e.key.toLowerCase() === 'f' && !isInputFocused(e)) {
        e.preventDefault();
        const isVisible = hud.style.display !== 'none';
        hud.style.display = isVisible ? 'none' : 'block';
        HapticAudio.themeChange();
      }
    });
  }

  // ---------------------------------------------------------------------------
  // 14. HELPER UTILITIES
  // ---------------------------------------------------------------------------
  function isInputFocused(e) {
    const active = document.activeElement;
    return active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.isContentEditable);
  }

  // ---------------------------------------------------------------------------
  // 15. INITIALIZATION SEQUENCE
  // ---------------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', () => {
    initThemeEngine();
    initHaloEngine();
    initSidebarResizer();
    initDesktopSidebarToggle();
    initMobileDrawer();
    initCollapsibleChapters();
    initSidebarFilters();
    initScrollSpy();
    initTheaterWorkbench();
    initCopyButtons();
    initSearchHUD();
    initDecisionMatrix();

    // KaTeX mathematical auto-rendering
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false }
        ],
        throwOnError: false
      });
    }

    // Audio toggle button
    const audioBtn = document.getElementById('audio-toggle-btn');
    if (audioBtn) {
      audioBtn.textContent = STATE.audioEnabled ? '🔊' : '🔇';
      audioBtn.addEventListener('click', () => {
        STATE.audioEnabled = !STATE.audioEnabled;
        localStorage.setItem('dp_audio_enabled', STATE.audioEnabled ? 'true' : 'false');
        audioBtn.textContent = STATE.audioEnabled ? '🔊' : '🔇';
        if (STATE.audioEnabled) HapticAudio.themeChange();
      });
    }

    // Proactively render visible diagrams (e.g. Master Relationships hero)
    setTimeout(() => {
      renderVisibleDiagrams();
    }, 100);
  });

})();

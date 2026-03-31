---
phase: 01
slug: ui-enhancement
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-31
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Playwright (e2e), Vitest (unit if added) |
| **Config file** | `frontend/vite.config.js` (existing) |
| **Quick run command** | `cd frontend && npm run build` |
| **Full suite command** | `cd frontend && npm run build && npm run lint` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npm run build` to verify no build errors
- **After every plan wave:** Run `npm run build && npm run lint`
- **Before `/gsd:verify-work`:** Full build must pass
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | D-03 (framer-motion) | build | `npm run build` | ✅ | ⬜ pending |
| 01-01-02 | 01 | 1 | D-07 (architecture) | build | `npm run build` | ✅ | ⬜ pending |
| 01-01-03 | 01 | 1 | D-09 (animations) | build | `npm run build` | ✅ | ⬜ pending |
| 01-01-04 | 01 | 1 | D-10 (code splitting) | build | `npm run build` | ✅ | ⬜ pending |
| 01-02-01 | 01 | 1 | D-13 (Modal) | build + manual | `npm run build` | ✅ | ⬜ pending |
| 01-02-02 | 01 | 1 | D-13 (Tooltip) | build + manual | `npm run build` | ✅ | ⬜ pending |
| 01-02-03 | 01 | 1 | D-13 (Accordion) | build + manual | `npm run build` | ✅ | ⬜ pending |
| 01-02-04 | 01 | 1 | D-13 (Form inputs) | build + manual | `npm run build` | ✅ | ⬜ pending |
| 01-03-01 | 01 | 2 | D-04 (ink wash) | visual | Manual review | ✅ | ⬜ pending |
| 01-03-02 | 01 | 2 | D-05 (overlays) | visual | Manual review | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

This is a frontend UI phase. No traditional test framework setup needed.

- [ ] `frontend/src/ui/` directory created with primitive components
- [ ] `frontend/src/animations/variants.js` created with shared variants
- [ ] `frontend/src/tokens/index.js` created for design tokens
- [ ] `frontend/src/components/PageTransition.jsx` wraps AnimatePresence

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Page transition animation | D-01 | Visual animation quality | Navigate between pages, observe smooth ink-wash reveal |
| Card hover lift effect | D-02 | Visual micro-interaction | Hover over cards, verify lift + shadow + glow |
| Form input focus state | D-13 | Visual + accessibility | Tab to input, verify vermilion ring |
| Ink wash atmosphere | D-04, D-05 | Visual aesthetic | Review pages for subtle ink gradients/overlays |
| Reduced motion mode | All animations | Accessibility | Enable `prefers-reduced-motion`, verify no animation |
| Mobile responsiveness | All components | Cross-device | Resize to mobile viewport, verify layout |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

---

*Generated from research: 01-RESEARCH.md §7*

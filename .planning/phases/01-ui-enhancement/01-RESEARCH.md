# Phase 1: UI Enhancement - Research

**Research Date:** 2026-03-31
**Phase:** 1 - UI Enhancement and Optimization

---

## 1. framer-motion v12 with React 19 / React Router v7

### Key Findings

**AnimatePresence Setup:**
- React Router v7 (react-router-dom v7) uses `<BrowserRouter>` with `<Routes>`. For page transitions, wrap the route content with AnimatePresence.
- `AnimatePresence` requires `mode="wait"` to wait for exit animation before mounting new page.
- With React 19, framer-motion v12 is compatible — no special adjustments needed.

**Page Transition Pattern:**
```jsx
// Wrap route components with motion.div
import { motion, AnimatePresence } from 'framer-motion';
import { useLocation } from 'react-router-dom';

const pageVariants = {
  initial: { opacity: 0, y: 10 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -10 }
};

// In component:
<AnimatePresence mode="wait">
  <motion.div
    key={location.pathname}
    variants={pageVariants}
    initial="initial"
    animate="animate"
    exit="exit"
    transition={{ duration: 0.3, ease: 'easeInOut' }}
  >
    {children}
  </motion.div>
</AnimatePresence>
```

**Ink Wash Reveal Effect:**
- Use `clip-path` animation with a custom SVG mask for the ink wash reveal effect described in UI-SPEC.
- Alternative: use `mask-image` with gradient and animate `mask-size` or `mask-position`.

**Spring Configs for Eastern Aesthetic:**
```js
const easternSpring = { type: 'spring', stiffness: 100, damping: 15 }; // Gentle, not bouncy
const pageSpring = { type: 'spring', stiffness: 80, damping: 20 }; // Smooth page transitions
```

**useReducedMotion:**
- Always wrap animations with `useReducedMotion()` hook from framer-motion to respect accessibility preferences.
- framer-motion v12 supports this natively.

---

## 2. Design System Architecture

### Recommended Structure

```
frontend/src/
├── ui/                    # Primitive components
│   ├── Button.jsx         # Enhanced from existing
│   ├── Input.jsx          # NEW
│   ├── Textarea.jsx       # NEW
│   ├── Select.jsx         # NEW
│   ├── Badge.jsx          # NEW
│   └── Spinner.jsx        # NEW
├── components/            # Composite components
│   ├── AnimatedCard.jsx   # NEW - replaces plain Card
│   ├── Modal.jsx          # NEW
│   ├── Tooltip.jsx        # NEW
│   ├── Accordion.jsx      # NEW
│   ├── ChatBubble.jsx     # NEW
│   ├── LoadingSkeleton.jsx # NEW
│   ├── ProgressRing.jsx   # NEW
│   └── StaggerContainer.jsx # NEW
├── layout/                # Layout components
│   ├── PageTransition.jsx # NEW - wraps AnimatePresence
│   ├── Navbar.jsx         # Enhanced from existing
│   └── PageWrapper.jsx    # NEW
├── animations/            # Shared animation primitives
│   ├── variants.js        # fadeIn, slideUp, staggerChildren, etc.
│   └── springs.js         # Shared spring configs
├── tokens/                # Design tokens
│   └── index.js           # CSS custom properties / JS tokens
├── pages/                 # Route pages (existing)
└── App.jsx                # Modified for code splitting
```

### Key Architecture Decisions

**Design Tokens:**
- Tailwind config already has colors/fonts. Extend with JS tokens for complex values.
- Add CSS custom properties for non-Tailwind values (animation durations, shadow depths).
- `src/tokens.js` can export both Tailwind-compatible values and CSS variable definitions.

**Animation Variants:**
```js
// src/animations/variants.js
export const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
};

export const slideUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

export const staggerChildren = {
  visible: {
    transition: { staggerChildren: 0.1 }
  }
};
```

---

## 3. Ink Wash / Eastern Aesthetic Implementation

### Ink Wash Effects

**Brush Stroke SVG Dividers:**
- Use inline SVG with `feTurbulence` filter for organic brush edges.
- Place as `::before` pseudo-element or standalone decorative component.
- Example brush stroke divider pattern:
```svg
<svg viewBox="0 0 200 10" className="w-full h-2">
  <path d="M0,5 Q50,0 100,5 T200,5" stroke="#2B2B2B" stroke-width="2" fill="none" opacity="0.3"/>
</svg>
```

**Paper Texture:**
- Already have noise texture in `index.css`. Layer with subtle gradient overlay.
- For cards: `bg-gradient-to-br from-rice-paper to-rice-paper/95` with noise at 3-5% opacity.

**Ink Spread Effect on Cards:**
- Use `::after` pseudo-element with radial gradient that expands on hover.
- Animation: `clip-path` or `transform: scale()` with `transform-origin: center`.

### Performance Considerations

- SVG filters are GPU-accelerated but can be expensive if overused.
- Use `will-change: transform` sparingly (only on elements that animate).
- Prefer CSS `opacity` and `transform` over layout-affecting properties.

---

## 4. Code Splitting with React.lazy + Suspense

### Implementation

```jsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import LoadingSkeleton from './components/LoadingSkeleton';

// Lazy load all pages except Home (per D-10)
const CraftLibrary = lazy(() => import('./pages/CraftLibrary'));
const KnowledgeCurator = lazy(() => import('./pages/KnowledgeCurator'));
const MasterWorkshop = lazy(() => import('./pages/MasterWorkshop'));
const MyPractice = lazy(() => import('./pages/MyPractice'));
const VisionMentor = lazy(() => import('./pages/VisionMentor'));
const ShadowPuppet = lazy(() => import('./pages/ShadowPuppet'));
const CreativeWorkshop = lazy(() => import('./pages/CreativeWorkshop'));

function App() {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <Router>
          <OmniOrchestrator />
          <Suspense fallback={<LoadingSkeleton variant="page" />}>
            <Routes>
              <Route path="/" element={<Intro />} />
              <Route path="/home" element={<Home />} />
              {/* Lazy loaded routes */}
              <Route path="/craft-library" element={<CraftLibrary />} />
              <Route path="/knowledge-curator" element={<KnowledgeCurator />} />
              {/* ... */}
            </Routes>
          </Suspense>
        </Router>
      </ToastProvider>
    </ErrorBoundary>
  );
}
```

### Preloading Strategies

- Use `React.lazy` with `/* webpackPrefetch: true */` comment for critical routes.
- Consider preloading VisionMentor and CreativeWorkshop when user hovers on nav items.
- Home page stays fully loaded (not code-split) per D-10.

### Vite Configuration

Vite handles code splitting automatically. No special Vite config needed for basic React.lazy + Suspense.

---

## 5. Component Patterns

### Enhanced Button (from existing Button.jsx)

```jsx
import { motion } from 'framer-motion';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  iconLeft,
  iconRight,
  className = '',
  ...props
}) => {
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-8 py-3 text-lg',
    lg: 'px-12 py-4 text-xl'
  };

  const baseStyles = "font-xiaowei tracking-widest rounded-sm transition-all";

  const variants = {
    primary: "bg-ink-black text-rice-paper hover:bg-vermilion",
    outline: "border border-ink-black/30 text-ink-black hover:border-ink-black hover:bg-ink-black/5",
    ghost: "text-ink-black hover:text-vermilion"
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.97 }}
      className={`${baseStyles} ${sizes[size]} ${variants[variant]} ${className}`}
      disabled={loading || props.disabled}
      {...props}
    >
      {loading ? '处理中...' : children}
    </motion.button>
  );
};
```

### New Form Input Pattern

```jsx
const Input = ({ error, className = '', ...props }) => {
  return (
    <input
      className={`
        w-full px-4 py-3 font-serif
        border border-ink-black/20 rounded-sm
        bg-white text-ink-black
        transition-all duration-200
        focus:outline-none focus:border-vermilion focus:ring-2 focus:ring-vermilion/20
        placeholder:text-charcoal/50
        ${error ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20' : ''}
        ${className}
      `}
      {...props}
    />
  );
};
```

### Modal Pattern

- Use `createPortal` to render to document.body.
- Trap focus within modal when open.
- Close on Escape key, backdrop click, and close button.
- Animate with `motion.div` with `AnimatePresence` for enter/exit.

### Tooltip Pattern

- Positioned with `getBoundingClientRect()` calculation or use `useFloating` from floating-ui if complex positioning needed.
- Use `framer-motion` for fade in/out with `opacity` and `scale`.
- Trigger: `onMouseEnter` / `onMouseLeave` (desktop) or `onClick` (mobile fallback).

### Accordion Pattern

- Use framer-motion `AnimatePresence` with `max-height` animation for smooth expand/collapse.
- Support both single-open and multi-open variants via `allowMultiple` prop.

---

## 6. Potential Pitfalls

### Animation Performance

1. **Mobile Performance:** framer-motion on mobile can stutter. Use `useReducedMotion` to disable complex animations on mobile.
2. **Layout Thrashing:** Only animate `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`.
3. **will-change Overuse:** Add `will-change: transform` only to elements actively animating, remove after.

### React Router v7 Compatibility

1. **V7 Changes:** react-router-dom v7 is now distributed as react-router v7 with file-based routing options. Current code uses v6 patterns with `<Routes>` which still work.
2. **AnimatePresence + Routes:** The current `<Routes>` structure works but needs to wrap content in `AnimatePresence` for transitions.

### Bundle Size

1. **framer-motion Size:** framer-motion is ~40kb gzipped. Lazy load it on first animation if concerned.
2. **Re-exporting:** Don't re-export all components from a single `index.js` — tree shaking works better with direct imports.

### Accessibility

1. **Keyboard Navigation:** All interactive elements must be keyboard accessible.
2. **Focus Management:** Modals and drawers must trap focus and restore it on close.
3. **Screen Readers:** Use `aria-live` regions for dynamic content (chat messages, toast notifications).

---

## 7. Validation Architecture

Based on the UI-SPEC's "Implementation Priorities" section:

### Must Have (Core)
1. Page transition wrapper with ink-wash effect
2. AnimatedCard component
3. Enhanced Button with variants, loading state
4. LoadingSkeleton component
5. framer-motion integration with reduced-motion support
6. Route-based code splitting

### Should Have (Enhancement)
7. StaggerContainer for list animations
8. ChatBubble component
9. Enhanced OmniOrchestrator
10. Scroll-triggered animations for Home page
11. Count-up animation for stats

### Nice to Have (Polish)
12. ProgressRing component
13. Keyboard shortcut overlay
14. Touch gesture support
15. Confetti for achievements

### Verification Strategy

**Performance Metrics:**
- FCP < 1.5s, LCP < 2.5s, TTI < 3.5s, CLS < 0.1
- Bundle analyzer to verify code splitting working

**Visual Testing:**
- Screenshot comparison for page transitions
- Reduced-motion mode verification
- Cross-browser testing (Chrome, Firefox, Safari)

**Functional Testing:**
- All routes load correctly
- Animations complete without jank
- Loading states display correctly
- Keyboard navigation works

---

## 8. Integration Points

### Files to Modify

| File | Changes |
|------|---------|
| `frontend/src/main.jsx` | Add Suspense wrapper, lazy load routes |
| `frontend/src/index.css` | Add animation utilities, ink-wash styles |
| `frontend/tailwind.config.js` | Add spacing tokens, new colors if needed |

### New Files

| File | Purpose |
|------|---------|
| `frontend/src/ui/Button.jsx` | Enhanced Button |
| `frontend/src/ui/Input.jsx` | Form Input |
| `frontend/src/ui/Textarea.jsx` | Form Textarea |
| `frontend/src/ui/Select.jsx` | Form Select |
| `frontend/src/ui/Badge.jsx` | Badge component |
| `frontend/src/ui/Spinner.jsx` | Loading spinner |
| `frontend/src/components/AnimatedCard.jsx` | Card with hover animation |
| `frontend/src/components/Modal.jsx` | Modal dialog |
| `frontend/src/components/Tooltip.jsx` | Tooltip component |
| `frontend/src/components/Accordion.jsx` | Accordion component |
| `frontend/src/components/ChatBubble.jsx` | Chat message bubble |
| `frontend/src/components/LoadingSkeleton.jsx` | Loading placeholder |
| `frontend/src/components/ProgressRing.jsx` | Circular progress |
| `frontend/src/components/StaggerContainer.jsx` | Stagger animation wrapper |
| `frontend/src/components/PageTransition.jsx` | Global page transitions |
| `frontend/src/animations/variants.js` | Shared animation variants |
| `frontend/src/animations/springs.js` | Shared spring configs |
| `frontend/src/tokens/index.js` | Design tokens |

### Files to Enhance (Not Replace)

- `frontend/src/components/Navbar.jsx` — Add scroll behavior, mobile drawer
- `frontend/src/components/OmniOrchestrator.jsx` — Add drag, keyboard shortcuts

---

## Research Summary

**What I need to know to PLAN this phase:**

1. **Animation:** framer-motion v12 works with React 19/RR7. AnimatePresence wraps content, not Routes. Ink-wash reveal via clip-path.
2. **Architecture:** Clear separation: `ui/` primitives, `components/` composites, `layout/` for wrappers, `animations/` for shared variants.
3. **Code Splitting:** React.lazy + Suspense in main.jsx, Home stays eager-loaded.
4. **Ink Wash:** SVG brush strokes as dividers, noise texture already present, layer ink effects carefully for performance.
5. **Components:** Modal needs portal + focus trap + Escape key, Tooltip needs positioning, Accordion needs height animation.
6. **Pitfalls:** Mobile animation performance, accessibility (focus management), bundle size of framer-motion.

**Confidence:** High — the codebase has good foundation (framer-motion installed, existing components with Eastern styling, Tailwind already configured).

---

*Researched: 2026-03-31*

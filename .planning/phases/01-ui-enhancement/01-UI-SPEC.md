# UI-SPEC.md - Phase 1: UI Enhancement & Animation Foundation

**Version:** 1.0
**Created:** 2026-03-31
**Project:** 数字传承人 (The Digital Inheritor)
**Tech Stack:** React 19 + TypeScript + Vite + Tailwind CSS + framer-motion

---

## 1. Design Language

### 1.1 Color System (No Changes Required)

The existing Eastern aesthetics color palette is well-defined and should be preserved:

| Token | Hex | Usage | Status |
|-------|-----|-------|--------|
| `ink-black` | `#2B2B2B` | Primary text, dark backgrounds | Keep |
| `rice-paper` | `#F7F5F0` | Light backgrounds, text on dark | Keep |
| `vermilion` | `#C04851` | Accent, CTAs, highlights | Keep |
| `cyan-glaze` | `#5796B3` | Vision Mentor agent accent | Keep |
| `tea-green` | `#CCD4BF` | Knowledge Curator agent accent | Keep |
| `charcoal` | `#4A4A4A` | Secondary text | Keep |

**Enhancement Recommendation:**
- Add a `gold-accent` (`#D4AF37`) for achievement/reward highlights (传承等级, badges)
- Add `shadow-ink` (`rgba(43,43,43,0.15)`) for deeper shadow effects

### 1.2 Typography (No Changes Required)

Existing font stack is appropriate:
- **书法体 (Ma Shan Zheng):** Headlines, hero text, decorative elements
- **小薇体 (ZCOOL XiaoWei):** Subheadings, card titles, UI labels
- **宋体 (Noto Serif SC):** Body text, paragraphs

**Enhancement:** Add `font-sans` utility override to use system-ui for better readability on small screens.

### 1.3 Spacing System

Maintain 4px base grid. Add these spacing tokens for consistent rhythm:
- `space-xs`: 8px (for tight elements)
- `space-sm`: 16px (default small gap)
- `space-md`: 24px (card padding)
- `space-lg`: 40px (section gaps)
- `space-xl`: 64px (page section separation)

### 1.4 Visual Assets

**Keep existing:**
- SVG noise texture background (already in index.css)
- Seal stamp decorative borders
- Ink spread effects on cards

**New additions for Phase 1:**
- Subtle ink wash brush stroke SVG dividers between sections
- Animated circular loader with vermilion stroke-dasharray
- Page transition curtain (ink wash reveal effect)

---

## 2. Animation Specs

### 2.1 Page Transitions

**Global Page Transition (AnimatePresence):**
- **Effect:** Ink wash reveal (clip-path animation)
- **Duration:** 500ms ease-in-out
- **Sequence:**
  1. 0-200ms: New page fades in with slight scale (0.98 → 1.0)
  2. 200-500ms: Ink wash curtain slides out from left to right
- **Implementation:** Wrap routes in `page-transition` div with framer-motion

**Individual Page Enter Animations:**

| Page | Animation | Duration | Easing |
|------|-----------|----------|--------|
| Home | Staggered fade-up for hero elements (100ms delay each) | 600ms total | ease-out |
| VisionMentor | Hand tracking canvas scales from 0.9 → 1 with fade | 400ms | spring(0.6) |
| KnowledgeCurator | Chat messages slide in from bottom, staggered 50ms | 300ms | ease-out |
| CreativeWorkshop | Tool panels slide from edges | 350ms | ease-in-out |
| CraftLibrary | Cards cascade in with 30ms stagger | 500ms | spring(0.8) |

### 2.2 Component Animations

#### Cards (Agent Cards, Feature Cards)

**Hover State:**
- Scale: 1.0 → 1.02
- Shadow: `0 4px 20px -2px rgba(43,43,43,0.1)` → `0 12px 40px -4px rgba(43,43,43,0.2)`
- Border glow: Add `box-shadow: 0 0 20px rgba(192,72,81,0.15)` on agent cards
- Chinese character watermark: opacity 0.1 → 0.2
- Duration: 300ms
- Easing: `cubic-bezier(0.4, 0, 0.2, 1)`

**Click/Active State:**
- Scale: 0.98 (press effect)
- Duration: 100ms
- Easing: ease-out

#### Buttons

**Primary Button (vermilion background):**
- Hover: brightness 1.1 + slight lift (translateY -2px) + shadow expansion
- Active: scale 0.97, brightness 0.95
- Disabled: opacity 0.5, cursor not-allowed
- Loading: pulse animation on spinner, text changes to 处理中...

**Outline Button:**
- Hover: background fills with 10% vermilion, border darkens
- Active: scale 0.97

#### Floating Action Button (OmniOrchestrator)

**Entry:** Scale from 0 → 1 with spring bounce (spring(0.5, 0.7))
**Pulse:** Subtle glow pulse every 5s when idle (opacity 0.8 → 1.0)
**Click:** Ripple effect emanating from center

#### Chat Messages

**User Message Enter:**
- Slide from right: x: 20px → 0, opacity: 0 → 1
- Duration: 250ms ease-out

**Assistant Message Enter:**
- Slide from left: x: -20px → 0, opacity: 0 → 1
- Duration: 300ms ease-out
- Stagger with typing indicator if showing

### 2.3 Micro-Interactions

**Form Inputs:**
- Focus: border transitions to vermilion with 2px ring (shadow: `0 0 0 3px rgba(192,72,81,0.2)`)
- Duration: 200ms

**Navigation Links:**
- Underline draws from left to right on hover
- Duration: 200ms ease-in-out

**Loading States:**
- Skeleton shimmer: gradient sweep animation (left to right, 1.5s loop)
- Use `bg-gradient-to-r from-transparent via-white/40 to-transparent`

**Success/Error Feedback:**
- Success: Checkmark icon draws itself (stroke-dashoffset animation, 400ms)
- Error: Subtle shake (translateX: 0 → -4px → 4px → 0, 300ms)

### 2.4 Decorative Animations

**Hero Section (Home):**
- Rotating concentric circles: Already exists, enhance to have subtle scale pulse
- Floating badge: Add gentle rotation (rotate: 0 → 3deg → -3deg → 0, 4s ease-in-out infinite)
- Background ink texture: Subtle parallax on scroll (translateY 10% slower than foreground)

**Agent Cards Watermark Characters (眼/知/艺):**
- Continuous slow rotation: 0deg → 360deg over 60s
- Opacity pulse: 0.08 → 0.12 over 3s

**Dashboard Stats Numbers:**
- Count-up animation when section enters viewport
- Duration: 1000ms with easing

---

## 3. Component Specs

### 3.1 Components to Enhance

#### PageTransition Wrapper
- **Purpose:** Global page transition orchestrator
- **Location:** `frontend/src/components/PageTransition.jsx` (NEW)
- **Props:** `children`, `className`
- **Behavior:** Wraps AnimatePresence around children with ink-wash reveal

#### AnimatedCard
- **Purpose:** Reusable card with hover animations
- **Location:** `frontend/src/components/AnimatedCard.jsx` (NEW)
- **Props:** `variant` (default | agent), `children`, `onClick`, `className`
- **States:** default, hover, active, disabled
- **Base styles:** Extends current `.card-shadow` with framer-motion

#### LoadingSkeleton
- **Purpose:** Shimmer loading placeholder
- **Location:** `frontend/src/components/LoadingSkeleton.jsx` (NEW)
- **Props:** `variant` (text | card | avatar | image), `count`, `className`
- **Animation:** Shimmer gradient sweep

#### StaggerContainer
- **Purpose:** Stagger children animations
- **Location:** `frontend/src/components/StaggerContainer.jsx` (NEW)
- **Props:** `children`, `staggerDelay` (default 100ms), `className`
- **Behavior:** Uses framer-motion `variants` with staggerChildren

#### ChatBubble
- **Purpose:** Standardized chat message bubble
- **Location:** `frontend/src/components/ChatBubble.jsx` (NEW)
- **Props:** `role` (user | assistant), `content`, `status` (sending | sent | error), `children`
- **Animation:** Slide-in based on role

#### ProgressRing
- **Purpose:** Circular progress indicator with Eastern aesthetic
- **Location:** `frontend/src/components/ProgressRing.jsx` (NEW)
- **Props:** `progress` (0-100), `size`, `strokeWidth`, `color`, `label`
- **Animation:** Draws on mount and on progress change

### 3.2 Components to Improve

#### Navbar
- **Current:** Static component
- **Enhancement:**
  - Add scroll-aware behavior (backdrop blur increases on scroll)
  - Add mobile hamburger menu with slide-in drawer from right
  - Animate active route indicator underline

#### Button
- **Current:** Basic variant (default, outline) + onClick
- **Enhancement:**
  - Add `size` prop (sm, md, lg)
  - Add `loading` state with spinner
  - Add `icon` slot (left/right)
  - Add ripple effect on click

#### OmniOrchestrator
- **Current:** Basic chat interface with expand/collapse
- **Enhancement:**
  - Add drag-to-reposition (framer-motion drag)
  - Add keyboard shortcuts (Cmd/Ctrl+K to toggle)
  - Add typing indicator with agent avatars
  - Animate task pipeline visualizer (currently static)

#### Card (Agent Cards in Home)
- **Current:** Basic hover shadow transition
- **Enhancement:**
  - Add staggered entrance animation when section scrolls into view
  - Add ink-spread effect on hover (pseudo-element)
  - Add subtle border glow matching agent color

### 3.3 Component Architecture

```
frontend/src/components/
├── ui/                          # Base UI components
│   ├── Button.jsx              # Enhanced with variants, sizes, loading
│   ├── AnimatedCard.jsx        # NEW: Card with hover animations
│   ├── LoadingSkeleton.jsx     # NEW: Shimmer placeholders
│   ├── ProgressRing.jsx        # NEW: Circular progress
│   └── ChatBubble.jsx          # NEW: Standardized chat bubbles
├── layout/
│   ├── PageTransition.jsx      # NEW: Global page transitions
│   ├── StaggerContainer.jsx    # NEW: Stagger animation wrapper
│   └── Navbar.jsx              # Enhanced with scroll behavior
├── orchestrator/
│   ├── OmniOrchestrator.jsx    # Enhanced with drag, shortcuts
│   └── TaskPipelineVisualizer.jsx  # Enhanced with animations
└── features/
    ├── HandTracking.jsx        # Enhanced with feedback animations
    └── ...
```

---

## 4. Interaction Patterns

### 4.1 Global Interactions

#### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Cmd/Ctrl + K` | Toggle OmniOrchestrator |
| `Cmd/Ctrl + /` | Show keyboard shortcut overlay |
| `Escape` | Close active modal/drawer/OmniOrchestrator |
| `Tab` | Navigate focusable elements |

#### Scroll Behavior
- Smooth scroll to sections on anchor click
- Intersection Observer triggers for:
  - Stagger animations on cards
  - Count-up on stats numbers
  - Lazy load images below fold
- Parallax on decorative elements (ink texture background)

### 4.2 Page-Specific Interactions

#### Home Page
1. **Hero CTA Buttons:**
   - Primary "开始修习" button: Navigates to CraftLibrary with ink-wash page transition
   - Secondary "皮影戏" button: Navigates to ShadowPuppet with same transition

2. **Agent Cards:**
   - Click anywhere on card navigates to respective agent page
   - Hover shows enhanced shadow + border glow
   - Agent accent color determines glow color (cyan-glaze, tea-green, vermilion)

3. **Dashboard Stats:**
   - Numbers animate from 0 to value when scrolled into view
   - Duration: 1000ms with ease-out

#### VisionMentor Page
1. **Camera Feed:**
   - Hand tracking canvas has subtle vignette overlay
   - Detection indicator pulses when hand detected

2. **Pose Analysis:**
   - Feedback appears with slide-in animation
   - Score ring draws on when result received
   - Color coding: red (0-50%), yellow (50-75%), green (75-100%)

3. **History Panel:**
   - Expandable cards with flip animation to show details
   - Timeline with animated connector lines

#### KnowledgeCurator Page
1. **Chat Interface:**
   - Messages slide in from appropriate side
   - Loading: Animated dots with "正在思考..." text
   - Sources expand with accordion animation

2. **Knowledge Graph Visualization:**
   - Nodes animate in with spring physics
   - Click node: Ripple effect + zoom
   - Drag: Momentum-based with friction

#### CreativeWorkshop Page
1. **Generation Pipeline:**
   - Step indicators animate sequentially (1 → 2 → 3)
   - Image reveals with fade + slight scale
   - Progress bar for generation: animated gradient

2. **Style Presets:**
   - Cards lift and glow on hover
   - Selected state: Persistent glow + checkmark overlay

### 4.3 Touch Interactions (Mobile)

- Swipe left/right to navigate between agent cards
- Long press on cards for quick actions menu
- Pinch to zoom on generated images
- Pull-to-refresh on history/practice pages

### 4.4 Feedback Patterns

#### Success States
- Green checkmark with draw animation (stroke-dashoffset: 100% → 0)
- Toast notification slides down from top, auto-dismisses after 3s
- Confetti burst for achievement unlocks

#### Error States
- Red shake animation (horizontal)
- Inline error message fades in below input
- Toast notification with retry action

#### Empty States
- Illustrated ink wash style SVG
- Encouraging message in calligraphy font
- CTA button to resolve empty state

---

## 5. Performance Contracts

### 5.1 Loading Performance

| Metric | Target | Strategy |
|--------|--------|----------|
| First Contentful Paint (FCP) | < 1.5s | Code-split pages, preload fonts |
| Largest Contentful Paint (LCP) | < 2.5s | Lazy load hero images, priority hints |
| Time to Interactive (TTI) | < 3.5s | Defer non-critical JS, skeleton loaders |
| Cumulative Layout Shift (CLS) | < 0.1 | Reserve space for images, no FOUC |

### 5.2 Animation Performance

**GPU Acceleration:**
- Use `transform` and `opacity` for all animations (no layout thrashing)
- Add `will-change: transform` to animated elements (sparingly)
- Prefer `translateX/Y` over `top/left` positioning

**Framer Motion Optimization:**
- Use `useReducedMotion` hook to respect accessibility preferences
- Lazy-load animation variants (dynamic import)
- Use `AnimatePresence` with `mode="wait"` for page transitions

**Target FPS:**
- All animations should maintain 60fps
- Drop to 30fps acceptable only for complex particle effects
- No frame drops during scroll animations

### 5.3 Bundle Optimization

- Route-based code splitting (React.lazy + Suspense)
- Dynamic import for:
  - framer-motion (loaded on first animation need)
  - Heavy components (VisionMentor camera, CreativeWorkshop tools)
  - markdown renderers (only on pages that need them)
- Image optimization:
  - WebP format with JPEG fallback
  - Responsive srcset for different viewports
  - Lazy loading with blur placeholder

### 5.4 Runtime Performance

- Virtualize long lists (practice history, craft library items) with `react-window`
- Memoize expensive computations (pose analysis results, RAG responses)
- Debounce scroll handlers (100ms threshold)
- Throttle animation frame updates where acceptable

### 5.5 Caching Strategy

- Static assets: Cache-Control max-age=31536000 (1 year)
- API responses: SWR or React Query for stale-while-revalidate
- Images: Service worker caching for offline access to viewed content

---

## 6. Responsive Strategy

### 6.1 Breakpoints

| Breakpoint | Width | Target |
|------------|-------|--------|
| `sm` | 640px | Large phones, small tablets |
| `md` | 768px | Tablets, small laptops |
| `lg` | 1024px | Desktops, large tablets landscape |
| `xl` | 1280px | Large desktops |
| `2xl` | 1536px | Extra large displays |

### 6.2 Layout Adaptations

#### Mobile-First (< 768px)
- Single column layouts
- Bottom navigation bar (replaces top Navbar)
- Full-width cards with reduced padding
- OmniOrchestrator: Full-screen modal instead of floating
- Simplified hero section (stacked layout, smaller typography)

#### Tablet (768px - 1024px)
- 2-column grids where appropriate
- Side navigation drawer
- Agent cards: 2-column layout
- Larger touch targets (min 44px)

#### Desktop (> 1024px)
- Full 3-column layouts for agent cards
- Persistent OmniOrchestrator as floating widget
- Hover states active
- Expanded navigation in header

### 6.3 Typography Scaling

| Element | Mobile | Desktop |
|---------|--------|---------|
| H1 (Hero) | 3rem | 5rem (8xl) |
| H2 (Section) | 1.875rem (2xl) | 2.25rem (3xl) |
| H3 (Card Title) | 1.25rem (xl) | 1.5rem (2xl) |
| Body | 1rem | 1.125rem |
| Small | 0.875rem | 0.875rem |

### 6.4 Component Responsive Behaviors

| Component | Mobile | Desktop |
|-----------|--------|---------|
| Navbar | Hamburger menu, slide-in drawer | Full nav links |
| OmniOrchestrator | Full-screen modal trigger | Floating widget |
| Agent Cards | Stack vertically | 3-column grid |
| Hero Image | Hidden or small | Full right-side visual |
| Chat Interface | Full-width bubbles | Max-width 70% |

### 6.5 Accessibility

- Minimum contrast ratio: 4.5:1 for body text, 3:1 for large text
- Focus indicators visible on all interactive elements
- Reduced motion: Disable complex animations via `prefers-reduced-motion`
- Screen reader announcements for dynamic content (live regions)
- Keyboard navigation for all interactive elements
- Touch targets: Minimum 44x44px on mobile

---

## Implementation Priorities

### Must Have (Phase 1 Core)
1. Page transition wrapper (ink-wash effect)
2. AnimatedCard component
3. Enhanced Button with variants
4. LoadingSkeleton component
5. Framer-motion integration with reduced-motion support
6. Performance: Route-based code splitting

### Should Have (Phase 1 Enhancement)
7. StaggerContainer for list animations
8. ChatBubble component
9. Enhanced OmniOrchestrator (drag, shortcuts)
10. Scroll-triggered animations for Home page
11. Count-up animation for stats

### Nice to Have (Phase 1 Polish)
12. ProgressRing component
13. Keyboard shortcut overlay
14. Touch gesture support
15. Confetti for achievements
16. Service worker for offline caching

---

*Document prepared for Phase 1 implementation. Updates to be made as design evolves.*

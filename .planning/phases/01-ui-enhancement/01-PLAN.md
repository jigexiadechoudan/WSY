---
phase: "01"
phase_name: UI Enhancement
plans_count: 1
waves: 2
requirements_addressed: []
generated: "2026-03-31"
generator: manual
---

# Phase 01 — Implementation Plan: UI Enhancement & Animation Foundation

**Phase:** 01
**Goal:** Enhance the 数字传承人 UI with Eastern aesthetics (ink wash style), page transitions + micro-interactions via framer-motion, component architecture reorganization into a formal design system, route-based code splitting, and essential new UI components (Modal, Tooltip, Accordion, Form inputs).

---

## Wave 1: Foundation (Design System + Code Splitting)

### 01-01: Animation Infrastructure

**Objective:** Set up framer-motion animation primitives, shared variants, and spring configs that all components will use.

**Files Modified:**
- `frontend/src/animations/variants.js` (NEW)
- `frontend/src/animations/springs.js` (NEW)

**Files to Read First:**
- `frontend/src/index.css` — existing utility classes and noise texture
- `frontend/package.json` — verify framer-motion v12 is installed
- `.planning/phases/01-ui-enhancement/01-RESEARCH.md` — animation patterns research

**Task:**
```markdown
<read_first>
- frontend/src/index.css
- frontend/package.json
- .planning/phases/01-ui-enhancement/01-RESEARCH.md
</read_first>

<action>
Create `frontend/src/animations/` directory with two files:

1. `variants.js` — Export shared animation variants:
   - `fadeIn`: { hidden: { opacity: 0 }, visible: { opacity: 1 } }
   - `fadeOut`: { hidden: { opacity: 1 }, visible: { opacity: 0 } }
   - `slideUp`: { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }
   - `slideDown`: { hidden: { opacity: 0, y: -20 }, visible: { opacity: 1, y: 0 } }
   - `slideLeft`: { hidden: { opacity: 0, x: 20 }, visible: { opacity: 1, x: 0 } }
   - `slideRight`: { hidden: { opacity: 0, x: -20 }, visible: { opacity: 1, x: 0 } }
   - `scaleIn`: { hidden: { opacity: 0, scale: 0.95 }, visible: { opacity: 1, scale: 1 } }
   - `staggerChildren`: { visible: { transition: { staggerChildren: 0.1 } } }
   - `pageTransition`: { initial: { opacity: 0, y: 10 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -10 } }

2. `springs.js` — Export shared spring configs:
   - `gentle`: { type: 'spring', stiffness: 100, damping: 15 }
   - `smooth`: { type: 'spring', stiffness: 80, damping: 20 }
   - `snappy`: { type: 'spring', stiffness: 300, damping: 30 }
   - `page`: { type: 'spring', stiffness: 80, damping: 20, duration: 0.3 }
   - `bouncy`: { type: 'spring', stiffness: 400, damping: 10 }

Export format:
   export const fadeIn = { ... }
   export const slideUp = { ... }
   // etc.

All variants use `transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }` as default unless specified.
</action>

<acceptance_criteria>
- [ ] `frontend/src/animations/variants.js` exists
- [ ] `frontend/src/animations/springs.js` exists
- [ ] All 9 variants exported: fadeIn, fadeOut, slideUp, slideDown, slideLeft, slideRight, scaleIn, staggerChildren, pageTransition
- [ ] All 5 spring configs exported: gentle, smooth, snappy, page, bouncy
- [ ] Variants include `hidden` and `visible` (or `initial`, `animate`, `exit`) states
- [ ] File can be imported: `import { fadeIn, slideUp, gentle } from '@/animations/variants'` (or `@/animations/springs`)
</acceptance_criteria>
```

---

### 01-02: Design Tokens

**Objective:** Create design token exports for colors, spacing, typography, and shadow values that can be used across components.

**Files Modified:**
- `frontend/src/tokens/index.js` (NEW)

**Files to Read First:**
- `frontend/tailwind.config.js` — existing color palette and font configuration
- `frontend/src/index.css` — existing utility classes (card-shadow, seal-border, vertical-text)

**Task:**
```markdown
<read_first>
- frontend/tailwind.config.js
- frontend/src/index.css
</read_first>

<action>
Create `frontend/src/tokens/index.js` exporting:

1. Color tokens (matching tailwind.config.js):
   - inkBlack: '#2B2B2B'
   - ricePaper: '#F7F5F0'
   - vermilion: '#C04851'
   - cyanGlaze: '#5796B3'
   - teaGreen: '#CCD4BF'
   - charcoal: '#4A4A4A'

2. Spacing tokens:
   - spaceXs: '8px'
   - spaceSm: '16px'
   - spaceMd: '24px'
   - spaceLg: '40px'
   - spaceXl: '64px'

3. Shadow depths:
   - shadowSm: '0 2px 8px -2px rgba(43,43,43,0.1)'
   - shadowMd: '0 4px 20px -2px rgba(43,43,43,0.1)'
   - shadowLg: '0 12px 40px -4px rgba(43,43,43,0.2)'
   - shadowGlow: '0 0 20px rgba(192,72,81,0.15)'

4. Animation durations:
   - durationFast: '150ms'
   - durationNormal: '300ms'
   - durationSlow: '500ms'

5. Easing curves:
   - easeDefault: [0.4, 0, 0.2, 1]
   - easeIn: [0.4, 0, 1, 1]
   - easeOut: [0, 0, 0.2, 1]

Export as named exports. Also export a `tokens` object containing all values.

Add CSS custom properties section at bottom (commented template for future use):
   /* CSS Custom Properties template:
   :root {
     --color-ink-black: #2B2B2B;
     ...
   }
   */
</action>

<acceptance_criteria>
- [ ] `frontend/src/tokens/index.js` exists
- [ ] All 6 color tokens exported
- [ ] All 5 spacing tokens exported
- [ ] All 4 shadow tokens exported
- [ ] Animation duration tokens exported
- [ ] Easing curve tokens exported
- [ ] Tokens object exported as default or named export
</acceptance_criteria>
```

---

### 01-03: UI Primitives — Button Enhancement

**Objective:** Enhance the existing Button component with framer-motion, size variants, loading state, and icon slots.

**Files Modified:**
- `frontend/src/components/Button.jsx` (REPLACE)

**Files to Read First:**
- `frontend/src/components/Button.jsx` (current implementation)
- `frontend/src/animations/variants.js` (new)
- `frontend/src/tokens/index.js` (new)

**Task:**
```markdown
<read_first>
- frontend/src/components/Button.jsx
- frontend/src/animations/variants.js
- frontend/src/tokens/index.js
</read_first>

<action>
Replace `frontend/src/components/Button.jsx` with enhanced version:

1. Props interface:
   - variant: 'primary' | 'outline' | 'ghost' (default: 'primary')
   - size: 'sm' | 'md' | 'lg' (default: 'md')
   - loading: boolean (default: false)
   - disabled: boolean (default: false)
   - iconLeft: React.ReactNode (optional)
   - iconRight: React.ReactNode (optional)
   - className: string (optional)
   - ...rest: other button props

2. Size classes:
   - sm: px-4 py-2 text-sm
   - md: px-8 py-3 text-lg (current)
   - lg: px-12 py-4 text-xl

3. Base styles: "font-xiaowei tracking-widest rounded-sm transition-all duration-200"

4. Variants (keep existing behavior):
   - primary: bg-ink-black text-rice-paper hover:bg-vermilion
   - outline: border border-ink-black/30 text-ink-black hover:border-ink-black hover:bg-ink-black/5
   - ghost: text-ink-black hover:text-vermilion

5. Wrap with framer-motion:
   - whileHover: scale 1.02, y -2 (if not loading/disabled)
   - whileTap: scale 0.97 (if not loading/disabled)
   - transition: { duration: 0.15 }

6. Loading state:
   - When loading=true, show '处理中...' text
   - Disable button when loading or disabled
   - Use cursor-not-allowed when disabled

7. Icon slots:
   - Render iconLeft before text if provided
   - Render iconRight after text if provided
   - Icons should be 1em size

Keep the component as default export.
</action>

<acceptance_criteria>
- [ ] Button accepts `variant` prop with values: primary, outline, ghost
- [ ] Button accepts `size` prop with values: sm, md, lg
- [ ] Button accepts `loading` prop that shows '处理中...' and disables click
- [ ] Button accepts `iconLeft` and `iconRight` props for inline icons
- [ ] framer-motion whileHover scales to 1.02 and y -2
- [ ] framer-motion whileTap scales to 0.97
- [ ] Disabled state uses cursor-not-allowed
- [ ] File exists at `frontend/src/components/Button.jsx`
- [ ] `import Button from '@/components/Button'` works
</acceptance_criteria>
```

---

### 01-04: Route-Based Code Splitting

**Objective:** Implement React.lazy + Suspense for all pages except Home, with LoadingSkeleton fallback.

**Files Modified:**
- `frontend/src/main.jsx` (MODIFY)

**Files to Read First:**
- `frontend/src/main.jsx` (current implementation)
- `frontend/src/pages/*.jsx` (all page files)
- `frontend/src/components/LoadingSkeleton.jsx` (or create if missing)

**Task:**
```markdown
<read_first>
- frontend/src/main.jsx
- frontend/src/pages/Home.jsx
- frontend/src/pages/CraftLibrary.jsx
- frontend/src/pages/KnowledgeCurator.jsx
- frontend/src/pages/VisionMentor.jsx
- frontend/src/pages/ShadowPuppet.jsx
- frontend/src/pages/CreativeWorkshop.jsx
- frontend/src/pages/MasterWorkshop.jsx
- frontend/src/pages/MyPractice.jsx
</read_first>

<action>
Modify `frontend/src/main.jsx`:

1. Add lazy imports (NOT for Home or Intro — these stay eager loaded per D-10):
   ```js
   const CraftLibrary = lazy(() => import('./pages/CraftLibrary'));
   const KnowledgeCurator = lazy(() => import('./pages/KnowledgeCurator'));
   const MasterWorkshop = lazy(() => import('./pages/MasterWorkshop'));
   const MyPractice = lazy(() => import('./pages/MyPractice'));
   const VisionMentor = lazy(() => import('./pages/VisionMentor'));
   const ShadowPuppet = lazy(() => import('./pages/ShadowPuppet'));
   const CreativeWorkshop = lazy(() => import('./pages/CreativeWorkshop'));
   ```

2. Import Suspense and LoadingSkeleton:
   ```js
   import { lazy, Suspense } from 'react';
   import LoadingSkeleton from './components/LoadingSkeleton';
   ```

3. Wrap ALL routes (or the Routes element) with a single Suspense boundary:
   ```jsx
   <Suspense fallback={<LoadingSkeleton variant="page" />}>
     <Routes>
       {/* All routes here */}
     </Routes>
   </Suspense>
   ```

4. If LoadingSkeleton.jsx doesn't exist, create a basic version first:
   - Variant: 'page' shows a full-page skeleton
   - Use `bg-ink-black/5` with shimmer animation
   - Use the existing noise texture from index.css if possible

Keep all existing imports (OmniOrchestrator, ToastProvider, ErrorBoundary, etc.).

Home and Intro routes should NOT be lazy loaded — they stay as direct imports.
</action>

<acceptance_criteria>
- [ ] All pages except Home and Intro use `lazy()` import
- [ ] Single Suspense boundary wraps all Routes
- [ ] Suspense fallback is LoadingSkeleton with variant="page"
- [ ] `npm run build` succeeds without errors
- [ ] Network tab shows separate chunks for lazy-loaded pages (build verification)
- [ ] LoadingSkeleton component exists at `frontend/src/components/LoadingSkeleton.jsx`
</acceptance_criteria>
```

---

### 01-05: PageTransition Wrapper Component

**Objective:** Create a wrapper component that provides consistent page transitions using AnimatePresence.

**Files Modified:**
- `frontend/src/components/PageTransition.jsx` (NEW)

**Files to Read First:**
- `frontend/src/animations/variants.js` (pageTransition variant)
- `frontend/package.json` (verify framer-motion)

**Task:**
```markdown
<read_first>
- frontend/src/animations/variants.js
- frontend/package.json
</read_first>

<action>
Create `frontend/src/components/PageTransition.jsx`:

1. Use `useLocation()` from react-router-dom to track route changes

2. Props:
   - children: React.ReactNode
   - className: string (optional)

3. Implementation:
   ```jsx
   import { motion, AnimatePresence } from 'framer-motion';
   import { useLocation } from 'react-router-dom';
   import { pageTransition } from '../animations/variants';

   function PageTransition({ children, className = '' }) {
     const location = useLocation();

     return (
       <AnimatePresence mode="wait" initial={false}>
         <motion.div
           key={location.pathname}
           className={className}
           initial="initial"
           animate="animate"
           exit="exit"
           variants={pageTransition}
         >
           {children}
         </motion.div>
       </AnimatePresence>
     );
   }
   ```

4. Export as default AND named export:
   ```js
   export { PageTransition };
   export default PageTransition;
   ```

5. Add JSDoc comment explaining purpose:
   /// Wraps page content with AnimatePresence for route-change transitions
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/PageTransition.jsx`
- [ ] Uses `AnimatePresence` with `mode="wait"`
- [ ] Uses `useLocation` to key the animated element
- [ ] Uses `pageTransition` variant from variants.js
- [ ] Exports as both default and named export
- [ ] `import PageTransition from '@/components/PageTransition'` works
</acceptance_criteria>
```

---

### 01-06: LoadingSkeleton Component

**Objective:** Create a reusable shimmer loading skeleton component with variants for page, card, text, avatar.

**Files Modified:**
- `frontend/src/components/LoadingSkeleton.jsx` (NEW)

**Files to Read First:**
- `frontend/src/index.css` (existing shimmer utility if any)

**Task:**
```markdown
<read_first>
- frontend/src/index.css
</read_first>

<action>
Create `frontend/src/components/LoadingSkeleton.jsx`:

1. Props:
   - variant: 'page' | 'card' | 'text' | 'avatar' (default: 'text')
   - count: number (default: 1) — for repeating skeleton items
   - className: string (optional)

2. Skeleton variants:
   - page: Full viewport height skeleton with header, sidebar, content areas
   - card: Rectangular card shape with title and text lines
   - text: Single or multiple text line(s) based on count prop
   - avatar: Circular placeholder

3. Shimmer animation:
   - Use `bg-gradient-to-r from-transparent via-white/40 to-transparent`
   - Animate with `animate: { backgroundPosition: ['200% 0', '-200% 0'] }`
   - Duration: 1.5s, repeat: infinite
   - Add `overflow-hidden` to container

4. Base skeleton style:
   - `bg-ink-black/5 rounded-sm`
   - Minimum height appropriate for variant

5. For 'text' variant with count > 1:
   - Render array of lines with decreasing width (100%, 80%, 60%)

Export as default.

Example usage:
   <LoadingSkeleton variant="card" count={3} />
   <LoadingSkeleton variant="page" />
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/LoadingSkeleton.jsx`
- [ ] Supports variant prop: page, card, text, avatar
- [ ] Supports count prop for repeating items
- [ ] Shimmer animation runs smoothly
- [ ] Uses rice-paper color with ink-black shimmer
- [ ] Export works: `import LoadingSkeleton from '@/components/LoadingSkeleton'`
</acceptance_criteria>
```

---

## Wave 2: Component Inventory

### 01-07: AnimatedCard Component

**Objective:** Create a card component with enhanced hover animations (lift, shadow expansion, border glow) for Agent cards.

**Files Modified:**
- `frontend/src/components/AnimatedCard.jsx` (NEW)

**Files to Read First:**
- `frontend/src/components/Card.jsx` (current implementation)
- `frontend/src/animations/variants.js` (for slideUp variant)
- `frontend/src/tokens/index.js` (shadow tokens)

**Task:**
```markdown
<read_first>
- frontend/src/components/Card.jsx
- frontend/src/animations/variants.js
- frontend/src/tokens/index.js
</read_first>

<action>
Create `frontend/src/components/AnimatedCard.jsx`:

1. Props:
   - variant: 'default' | 'agent' (default: 'default')
   - agentColor: string (optional, for agent variant glow — hex color)
   - children: React.ReactNode
   - className: string (optional)
   - onClick: function (optional)
   - ...props: other div props

2. Default variant hover:
   - scale: 1.02
   - y: -4
   - shadow transition to shadowLg from shadowMd
   - duration: 300ms

3. Agent variant hover (additional):
   - Border glow using agentColor prop (default: vermilion)
   - Chinese character watermark opacity 0.1 → 0.2
   - Use box-shadow with color: `0 0 20px rgba(${agentColor}, 0.15)`

4. Implementation with framer-motion:
   - Use `motion.div` with whileHover and whileTap
   - Initial shadow from shadowMd token
   - Hover shadow from shadowLg token
   - Use `transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }`

5. Base styles:
   - bg-white rounded-sm overflow-hidden relative
   - Apply card-shadow class from index.css as base

Export as default.

Example:
   <AnimatedCard variant="agent" agentColor="#C04851">
     <h3>视觉导师</h3>
     <p>学习手势追踪</p>
   </AnimatedCard>
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/AnimatedCard.jsx`
- [ ] Props: variant ('default'|'agent'), agentColor, children, className, onClick
- [ ] Default variant: hover lifts 4px, shadow expands, scale 1.02
- [ ] Agent variant: includes border glow with agentColor
- [ ] Press effect: scale 0.98
- [ ] Transition duration 300ms with ease [0.4, 0, 0.2, 1]
- [ ] Export works: `import AnimatedCard from '@/components/AnimatedCard'`
</acceptance_criteria>
```

---

### 01-08: Modal Component

**Objective:** Create an accessible Modal/Dialog component with overlay, close button, escape key support, and framer-motion enter/exit animations.

**Files Modified:**
- `frontend/src/components/Modal.jsx` (NEW)

**Files to Read First:**
- `frontend/src/animations/variants.js` (scaleIn variant)

**Task:**
```markdown
<read_first>
- frontend/src/animations/variants.js
</read_first>

<action>
Create `frontend/src/components/Modal.jsx`:

1. Props:
   - isOpen: boolean (required — controlled)
   - onClose: function (required — called when backdrop, X, or Escape pressed)
   - title: string (optional)
   - children: React.ReactNode
   - size: 'sm' | 'md' | 'lg' (default: 'md')
   - showCloseButton: boolean (default: true)
   - closeOnBackdrop: boolean (default: true)
   - closeOnEscape: boolean (default: true)
   - className: string (optional)

2. Portal rendering:
   - Use `createPortal` to render to document.body
   - Use `useEffect` to create/destroy portal div

3. Animation:
   - Backdrop: fadeIn variant, opacity 0 → 0.5 bg-ink-black/80
   - Modal: scaleIn variant with slideUp
   - Exit: reverse the above

4. Backdrop:
   - Fixed inset-0 with bg-ink-black/80 backdrop-blur-sm
   - onClick: call onClose if closeOnBackdrop
   - z-index: 50

5. Modal panel:
   - bg-white rounded-sm shadowLg
   - centered with flexbox
   - max-width by size: sm=400px, md=500px, lg=700px
   - p-6 spacing
   - z-index: 51

6. Close button:
   - Top-right corner, absolute positioned
   - Use X icon or '×' character
   - Hover: vermilion color

7. Keyboard handling:
   - useEffect with keydown listener for Escape
   - Clean up listener on unmount

8. Body scroll lock:
   - When open, set document.body.style.overflow = 'hidden'
   - Restore on close/unmount

Export as default.
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/Modal.jsx`
- [ ] Renders via createPortal to document.body
- [ ] Props: isOpen, onClose, title, children, size
- [ ] Backdrop click closes modal (if closeOnBackdrop=true)
- [ ] Escape key closes modal (if closeOnEscape=true)
- [ ] framer-motion enter/exit animations work
- [ ] Body scroll locks when open
- [ ] Close button visible and functional
- [ ] Export works: `import Modal from '@/components/Modal'`
</acceptance_criteria>
```

---

### 01-09: Tooltip Component

**Objective:** Create a Tooltip component with positioning, hover-triggered visibility, and framer-motion fade animation.

**Files Modified:**
- `frontend/src/components/Tooltip.jsx` (NEW)

**Files to Read First:**
- `frontend/src/animations/variants.js` (fadeIn/fadeOut)

**Task:**
```markdown
<read_first>
- frontend/src/animations/variants.js
</read_first>

<action>
Create `frontend/src/components/Tooltip.jsx`:

1. Props:
   - content: React.ReactNode | string (required — tooltip text)
   - children: React.ReactNode (required — the trigger element)
   - position: 'top' | 'bottom' | 'left' | 'right' (default: 'top')
   - delay: number (default: 200 — ms before showing)
   - className: string (optional)
   - tooltipClassName: string (optional)

2. Positioning logic:
   - Use CSS-only positioning with absolute + transforms
   - top: bottom-full + translateX(-50%), mb-2
   - bottom: top-full + translateX(-50%), mt-2
   - left: right-full + translateY(-50%), mr-2
   - right: left-full + translateY(-50%), ml-2

3. Trigger:
   - Wrap children in relative positioned span
   - Use onMouseEnter + onMouseLeave for show/hide
   - Delay timer for hide

4. Animation:
   - Show: fadeIn + scale from 0.95 → 1
   - Hide: fadeOut + scale from 1 → 0.95
   - Duration: 150ms

5. Tooltip styles:
   - bg-ink-black text-rice-paper
   - px-3 py-2 rounded-sm text-sm font-xiaowei
   - max-width: 250px
   - z-50
   - pointer-events: none

6. Accessibility:
   - Add role="tooltip" to tooltip element
   - Add aria-describedby to children (use generated ID)
   - Not focusable (pointer-events: none)

Export as default.
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/Tooltip.jsx`
- [ ] Props: content, children, position, delay
- [ ] Positions correctly: top, bottom, left, right
- [ ] Shows on hover with configurable delay
- [ ] Hides when mouse leaves
- [ ] framer-motion fade + scale animation
- [ ] Aria attributes for accessibility
- [ ] Export works: `import Tooltip from '@/components/Tooltip'`
</acceptance_criteria>
```

---

### 01-10: Accordion Component

**Objective:** Create an Accordion/Collapsible component with animated expand/collapse, single or multi-open variants.

**Files Modified:**
- `frontend/src/components/Accordion.jsx` (NEW)

**Files to Read First:**
- `frontend/src/animations/variants.js` (for animation reference)

**Task:**
```markdown
<read_first>
- frontend/src/animations/variants.js
</read_first>

<action>
Create `frontend/src/components/Accordion.jsx`:

1. AccordionItem sub-component:
   Props:
   - title: string | React.ReactNode (required)
   - children: React.ReactNode (required)
   - defaultOpen: boolean (default: false)
   - className: string (optional)

2. Accordion wrapper component:
   Props:
   - children: React.ReactNode (AccordionItem components)
   - allowMultiple: boolean (default: false) — allow multiple items open
   - className: string (optional)

3. Implementation pattern:
   - Use `useState` for open/closed state per item
   - Track open items array for allowMultiple mode

4. Animation with AnimatePresence + max-height:
   - Container: `overflow-hidden transition-all duration-300`
   - Use `style={{ maxHeight: isOpen ? contentHeight : 0 }}`
   - Measure content height with `useRef` and `scrollHeight`

5. Header styles:
   - flex justify-between items-center
   - py-3 px-4
   - bg-rice-paper hover:bg-ink-black/5
   - cursor-pointer
   - Chevron icon rotates 180deg when open

6. Content styles:
   - px-4 pb-3
   - text-charcoal font-serif

7. Accessibility:
   - Use `<button>` for header (keyboard accessible)
   - aria-expanded on header button
   - aria-controls linking to content panel

Export Accordion and AccordionItem.

Example:
   <Accordion allowMultiple>
     <AccordionItem title="什么是皮影戏？">
       <p>皮影戏是一种...</p>
     </AccordionItem>
     <AccordionItem title="如何学习？">
       <p>跟随以下步骤...</p>
     </AccordionItem>
   </Accordion>
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/Accordion.jsx`
- [ ] Exports Accordion and AccordionItem components
- [ ] allowMultiple prop works (multiple items can be open)
- [ ] Single-open mode works (opening one closes others)
- [ ] Expand/collapse animation is smooth
- [ ] Chevron icon rotates on open/close
- [ ] Keyboard accessible (Enter/Space toggles)
- [ ] Export works: `import { Accordion, AccordionItem } from '@/components/Accordion'`
</acceptance_criteria>
```

---

### 01-11: Form Input Components

**Objective:** Create Input, Textarea, and Select components with consistent Eastern aesthetic styling, focus states, and error states.

**Files Modified:**
- `frontend/src/ui/Input.jsx` (NEW)
- `frontend/src/ui/Textarea.jsx` (NEW)
- `frontend/src/ui/Select.jsx` (NEW)

**Files to Read First:**
- `frontend/tailwind.config.js` (colors)
- `frontend/src/tokens/index.js` (if exists)

**Task:**
```markdown
<read_first>
- frontend/tailwind.config.js
</read_first>

<action>
Create `frontend/src/ui/Input.jsx`:

1. Props:
   - label: string (optional)
   - error: string (optional — error message)
   - className: string (optional)
   - ...inputProps: standard input attributes

2. Base input styles:
   - w-full px-4 py-3
   - font-serif text-ink-black
   - border border-ink-black/20 rounded-sm
   - bg-white
   - transition-all duration-200

3. Focus state:
   - border-vermilion
   - ring-2 ring-vermilion/20
   - outline-none

4. Error state:
   - border-red-500
   - ring-2 ring-red-500/20
   - If error prop provided, show red text below

5. Label:
   - font-xiaowei text-sm text-charcoal
   - mb-1 above input
   - Required indicator: text-vermilion after label text

Create `frontend/src/ui/Textarea.jsx`:

1. Same props as Input
2. Same styling as Input
3. Add: min-h-32, resize-vertical

Create `frontend/src/ui/Select.jsx`:

1. Same props as Input (minus error for now)
2. Same base styling as Input
3. Use native <select> with custom arrow
4. Arrow: absolute right-3 top-1/2 -translate-y-1/2
   - Use SVG chevron or '▼' character

Export all three components.
</action>

<acceptance_criteria>
- [ ] `frontend/src/ui/Input.jsx` exists
- [ ] `frontend/src/ui/Textarea.jsx` exists
- [ ] `frontend/src/ui/Select.jsx` exists
- [ ] Input accepts: label, error, className, standard input props
- [ ] Textarea accepts same props, has min-height and resize
- [ ] Select shows custom chevron arrow
- [ ] Focus shows vermilion ring
- [ ] Error shows red border and error message text
- [ ] All export correctly from `@/ui/Input`, `@/ui/Textarea`, `@/ui/Select`
</acceptance_criteria>
```

---

### 01-12: StaggerContainer Component

**Objective:** Create a container component that staggers the animation of its children when they enter the viewport.

**Files Modified:**
- `frontend/src/components/StaggerContainer.jsx` (NEW)

**Files to Read First:**
- `frontend/src/animations/variants.js` (staggerChildren, slideUp)

**Task:**
```markdown
<read_first>
- frontend/src/animations/variants.js
</read_first>

<action>
Create `frontend/src/components/StaggerContainer.jsx`:

1. Props:
   - children: React.ReactNode (typically motion.div items)
   - staggerDelay: number (default: 0.1 — seconds between each child)
   - className: string (optional)
   - initial: string (default: 'hidden') — initial animation state
   - animate: string (default: 'visible') — final animation state
   - variants: object (optional — override default variants)

2. Default variants (if not provided):
   - container: { visible: { transition: { staggerChildren: staggerDelay } } }
   - child: { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }

3. Implementation:
   - Use `motion.div` as container with container variants
   - Children should be `motion.div` with child variants
   - Use `framer-motion`'s `variants` prop inheritance

4. Optional viewport trigger:
   - Add `viewport={{ once: true, margin: '-100px' }}` to container
   - This triggers animation when container enters viewport

Example usage:
   <StaggerContainer staggerDelay={0.1}>
     <motion.div variants={childVariants}>Item 1</motion.div>
     <motion.div variants={childVariants}>Item 2</motion.div>
     <motion.div variants={childVariants}>Item 3</motion.div>
   </StaggerContainer>

Export as default.
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/StaggerContainer.jsx`
- [ ] Props: children, staggerDelay, className, variants, initial, animate
- [ ] Children animate with staggered delay
- [ ] Viewport trigger works (once: true)
- [ ] Default child variants: opacity 0→1, y 20→0
- [ ] Export works: `import StaggerContainer from '@/components/StaggerContainer'`
</acceptance_criteria>
```

---

### 01-13: ChatBubble Component

**Objective:** Create a standardized chat message bubble component for the KnowledgeCurator chat interface.

**Files Modified:**
- `frontend/src/components/ChatBubble.jsx` (NEW)

**Files to Read First:**
- `frontend/src/animations/variants.js` (slideLeft, slideRight)

**Task:**
```markdown
<read_first>
- frontend/src/animations/variants.js
</read_first>

<action>
Create `frontend/src/components/ChatBubble.jsx`:

1. Props:
   - role: 'user' | 'assistant' (required)
   - content: string | React.ReactNode (required)
   - status: 'sending' | 'sent' | 'error' (default: 'sent')
   - children: React.ReactNode (optional — alternative to content)
   - className: string (optional)

2. User bubble styles (right-aligned):
   - bg-vermilion text-rice-paper
   - rounded-ee-sm rounded-es-lg
   - max-w-[70%] ml-auto

3. Assistant bubble styles (left-aligned):
   - bg-ink-black/5 text-ink-black
   - rounded-es-sm rounded-ee-lg
   - max-w-[70%] mr-auto

4. Animation:
   - User: slideRight variant (x: 20 → 0)
   - Assistant: slideLeft variant (x: -20 → 0)
   - Duration: 250ms for user, 300ms for assistant

5. Status indicators:
   - sending: show animated typing dots (3 dots pulsing)
   - sent: no indicator
   - error: show red '!' icon, retry callback if needed

6. Timestamp (optional prop):
   - Show time below bubble
   - text-xs text-charcoal/50

Export as default.
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/ChatBubble.jsx`
- [ ] Props: role (user/assistant), content, status, timestamp
- [ ] User bubbles right-aligned, vermilion background
- [ ] Assistant bubbles left-aligned, ink-black/5 background
- [ ] framer-motion slide-in animation based on role
- [ ] Status 'sending' shows typing indicator
- [ ] Export works: `import ChatBubble from '@/components/ChatBubble'`
</acceptance_criteria>
```

---

### 01-14: Navbar Enhancement

**Objective:** Enhance the existing Navbar with scroll-aware backdrop blur, mobile hamburger menu, and animated active route indicator.

**Files Modified:**
- `frontend/src/components/Navbar.jsx` (ENHANCE)

**Files to Read First:**
- `frontend/src/components/Navbar.jsx` (current implementation)

**Task:**
```markdown
<read_first>
- frontend/src/components/Navbar.jsx
</read_first>

<action>
Enhance `frontend/src/components/Navbar.jsx`:

1. Scroll-aware backdrop blur:
   - Track scroll position with `useState` + `useEffect` + scroll listener
   - When scrolled > 50px: add `backdrop-blur-md bg-rice-paper/90`
   - When at top: transparent or `bg-rice-paper/50`

2. Mobile hamburger menu:
   - Add state: `isMobileMenuOpen` (default: false)
   - Hamburger button visible on mobile (md: hidden)
   - When open: slide-in drawer from right
   - Use framer-motion AnimatePresence for open/close
   - Full height overlay with nav links

3. Active route indicator:
   - Use `useLocation` to get current path
   - Active link: vermilion text color
   - Animated underline that slides to active link
   - Use `motion.div` with `layoutId` for shared transition

4. Keep existing nav links structure:
   - Home, Craft Library, Vision Mentor, Knowledge Curator, Creative Workshop
   - My Practice link

5. Preserve existing styles:
   - Eastern aesthetic (fonts, colors)
   - Responsive behavior

6. Accessibility:
   - Hamburger button: aria-label="Open menu"
   - Mobile menu: aria-expanded, role="navigation"
</action>

<acceptance_criteria>
- [ ] File exists at `frontend/src/components/Navbar.jsx`
- [ ] Scroll > 50px increases backdrop blur
- [ ] Hamburger menu visible on mobile
- [ ] Mobile menu slides in from right with overlay
- [ ] Active route has vermilion color and animated underline
- [ ] Keyboard accessible hamburger button
- [ ] Export works: `import Navbar from '@/components/Navbar'`
</acceptance_criteria>
```

---

## Verification

### Build Verification
```bash
cd frontend
npm run build  # Must succeed with no errors
```

### Lint Verification
```bash
cd frontend
npm run lint  # Must pass with no errors
```

### Visual Checklist (Manual)
- [ ] Page transitions animate smoothly between routes
- [ ] Cards lift on hover with shadow expansion
- [ ] Agent cards have vermilion border glow on hover
- [ ] Form inputs show vermilion ring on focus
- [ ] Modal appears with scale-in animation, closes on Escape
- [ ] Tooltip shows on hover with fade animation
- [ ] Accordion expands/collapses smoothly
- [ ] Navbar blur increases on scroll
- [ ] Mobile hamburger menu works
- [ ] Loading skeleton shows during page load
- [ ] All animations respect reduced-motion preference

---

## must_haves (Goal-Backward Verification)

From ROADMAP goal: "增强东方美学风格, 添加炫酷动画/过渡效果, 性能优化（加载速度、渲染）, 提升可维护性和可扩展性"

| Must Have | Verification |
|-----------|-------------|
| Eastern aesthetics enhanced | Ink wash SVG elements, paper texture, vermilion accents preserved |
| Page transitions | AnimatePresence wraps routes, ink-wash reveal effect |
| Micro-interactions | Button press, card hover, form focus all animated |
| framer-motion primary | CSS transitions for simple states, framer-motion for complex |
| Design system structure | `src/ui/`, `src/components/`, `src/layout/`, `src/animations/` |
| Design tokens | `src/tokens/index.js` exports colors, spacing, shadows |
| Route code splitting | React.lazy for all pages except Home |
| Modal component | Portal, Escape key, backdrop click, animations |
| Tooltip component | Hover trigger, 4 positions, fade animation |
| Accordion component | Expand/collapse, single/multi-open |
| Form inputs | Input, Textarea, Select with focus/error states |
| Bundle optimization | Separate chunks for lazy-loaded pages |
| Loading skeleton | Shimmer animation, page/card/text variants |

---

*Plan generated: 2026-03-31*
*Wave 1: Tasks 01-01 through 01-06*
*Wave 2: Tasks 01-07 through 01-14*

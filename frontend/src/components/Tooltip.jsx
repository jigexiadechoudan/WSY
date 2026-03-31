/**
 * Tooltip Component
 * Hover-triggered tooltip with positioning and fade animation
 */

import React, { useState, useRef, useId } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const Tooltip = ({
  content,
  children,
  position = 'top',
  delay = 200,
  className = '',
  tooltipClassName = '',
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const timeoutRef = useRef(null);
  const tooltipId = useId();

  const showTooltip = () => {
    timeoutRef.current = setTimeout(() => {
      setIsVisible(true);
    }, delay);
  };

  const hideTooltip = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    setIsVisible(false);
  };

  const positionClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  };

  const arrowClasses = {
    top: 'top-full left-1/2 -translate-x-1/2 border-t-ink-black border-x-transparent border-b-transparent',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-b-ink-black border-x-transparent border-t-transparent',
    left: 'left-full top-1/2 -translate-y-1/2 border-l-ink-black border-y-transparent border-r-transparent',
    right: 'right-full top-1/2 -translate-y-1/2 border-r-ink-black border-y-transparent border-l-transparent',
  };

  const fadeInVariants = {
    hidden: { opacity: 0, scale: 0.95 },
    visible: { opacity: 1, scale: 1, transition: { duration: 0.15, ease: [0.4, 0, 0.2, 1] } },
    exit: { opacity: 0, scale: 0.95, transition: { duration: 0.15, ease: [0.4, 0, 0.2, 1] } }
  };

  return (
    <span className={`relative inline-flex ${className}`}>
      <span
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        aria-describedby={isVisible ? tooltipId : undefined}
      >
        {children}
      </span>

      <AnimatePresence>
        {isVisible && (
          <motion.span
            id={tooltipId}
            role="tooltip"
            className={`absolute z-50 px-3 py-2 bg-ink-black text-rice-paper rounded-sm text-sm font-xiaowei max-w-[250px] pointer-events-none whitespace-nowrap ${positionClasses[position]} ${tooltipClassName}`}
            variants={fadeInVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
          >
            {content}
            {/* Arrow */}
            <span
              className={`absolute w-0 h-0 border-4 ${arrowClasses[position]}`}
            />
          </motion.span>
        )}
      </AnimatePresence>
    </span>
  );
};

export default Tooltip;

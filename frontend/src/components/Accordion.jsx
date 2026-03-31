/**
 * Accordion Component
 * Animated expand/collapse with single or multi-open variants
 */

import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const AccordionItem = ({
  title,
  children,
  defaultOpen = false,
  className = '',
  isOpen,
  onToggle,
}) => {
  const contentRef = useRef(null);
  const [contentHeight, setContentHeight] = useState(0);

  useEffect(() => {
    if (contentRef.current) {
      setContentHeight(contentRef.current.scrollHeight);
    }
  }, [children]);

  const isControlled = isOpen !== undefined;
  const isItemOpen = isControlled ? isOpen : defaultOpen;

  const handleToggle = () => {
    if (onToggle) {
      onToggle();
    }
  };

  const contentVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] } },
    exit: { opacity: 0, transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] } }
  };

  return (
    <div className={`border border-ink-black/10 rounded-sm overflow-hidden ${className}`}>
      {/* Header */}
      <button
        onClick={handleToggle}
        className="w-full flex justify-between items-center py-3 px-4 bg-rice-paper hover:bg-ink-black/5 cursor-pointer transition-colors"
        aria-expanded={isItemOpen}
      >
        <span className="font-xiaowei text-ink-black text-left">{title}</span>
        <motion.span
          className="text-charcoal text-lg ml-4"
          animate={{ rotate: isItemOpen ? 180 : 0 }}
          transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
        >
          ▾
        </motion.span>
      </button>

      {/* Content */}
      <AnimatePresence initial={false}>
        {isItemOpen && (
          <motion.div
            initial={{ opacity: 0, maxHeight: 0 }}
            animate={{ opacity: 1, maxHeight: contentHeight }}
            exit={{ opacity: 0, maxHeight: 0 }}
            transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
            style={{ overflow: 'hidden' }}
          >
            <div
              ref={contentRef}
              className="px-4 pb-3 text-charcoal font-serif"
            >
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

const Accordion = ({
  children,
  allowMultiple = false,
  className = '',
}) => {
  // Convert children to array and extract defaultOpen states
  const items = React.Children.map(children, (child, index) => {
    if (!child) return null;
    return {
      id: index,
      child,
      defaultOpen: child.props?.defaultOpen || false,
    };
  }).filter(Boolean);

  const [openItems, setOpenItems] = useState(() => {
    const initial = {};
    items.forEach(({ id, defaultOpen }) => {
      if (defaultOpen) initial[id] = true;
    });
    return initial;
  });

  const handleToggle = (id) => {
    setOpenItems((prev) => {
      if (allowMultiple) {
        const newState = { ...prev };
        if (newState[id]) {
          delete newState[id];
        } else {
          newState[id] = true;
        }
        return newState;
      } else {
        // Single open mode - close others
        const newState = {};
        if (!prev[id]) {
          newState[id] = true;
        }
        return newState;
      }
    });
  };

  return (
    <div className={`flex flex-col gap-2 ${className}`}>
      {items.map(({ id, child }) => (
        <AccordionItem
          key={id}
          isOpen={openItems[id]}
          onToggle={() => handleToggle(id)}
          title={child.props?.title}
        >
          {child.props?.children}
        </AccordionItem>
      ))}
    </div>
  );
};

// Named export for AccordionItem
export { AccordionItem };
export default Accordion;

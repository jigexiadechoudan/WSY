/**
 * StaggerContainer Component
 * Container that staggers animation of its children when entering viewport
 */

import React from 'react';
import { motion } from 'framer-motion';

const StaggerContainer = ({
  children,
  staggerDelay = 0.1,
  className = '',
  initial = 'hidden',
  animate = 'visible',
  variants,
}) => {
  // Default container variants
  const containerVariants = variants || {
    visible: {
      transition: {
        staggerChildren: staggerDelay,
      },
    },
  };

  // Default child variants
  const childVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.3,
        ease: [0.4, 0, 0.2, 1],
      },
    },
  };

  return (
    <motion.div
      className={className}
      variants={containerVariants}
      initial={initial}
      animate={animate}
      viewport={{ once: true, margin: '-100px' }}
    >
      {React.Children.map(children, (child) => {
        if (!child) return null;

        // If child is already a motion.div, apply child variants
        if (React.isValidElement(child) && child.type === motion.div) {
          return React.cloneElement(child, {
            variants: child.props.variants || childVariants,
          });
        }

        // Wrap non-motion elements
        return (
          <motion.div variants={childVariants}>
            {child}
          </motion.div>
        );
      })}
    </motion.div>
  );
};

export default StaggerContainer;

/**
 * AnimatedCard Component
 * Card with enhanced hover animations (lift, shadow expansion, border glow)
 * For Agent cards in 数字传承人
 */

import React from 'react';
import { motion } from 'framer-motion';
import { inkBlack, ricePaper, vermilion } from '../tokens/index';

const AnimatedCard = ({
  variant = 'default',
  agentColor = vermilion,
  children,
  className = '',
  onClick,
  ...props
}) => {
  const baseStyles = 'bg-white rounded-sm overflow-hidden relative cursor-pointer';

  // Default variant: lift + shadow expansion
  const defaultHover = {
    scale: 1.02,
    y: -4,
    boxShadow: '0 12px 40px -4px rgba(43,43,43,0.2)',
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  };

  const defaultInitial = {
    boxShadow: '0 4px 20px -2px rgba(43,43,43,0.1)',
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  };

  // Agent variant: border glow + watermark
  const agentGlow = `0 0 20px rgba(${agentColor}, 0.15)`;

  const agentHover = {
    scale: 1.02,
    y: -4,
    boxShadow: `0 12px 40px -4px rgba(43,43,43,0.2), ${agentGlow}`,
    borderColor: agentColor,
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  };

  const agentInitial = {
    boxShadow: '0 4px 20px -2px rgba(43,43,43,0.1)',
    borderColor: 'transparent',
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  };

  const whileTap = { scale: 0.98 };

  if (variant === 'agent') {
    return (
      <motion.div
        className={`${baseStyles} border ${className}`}
        style={{ borderColor: 'transparent' }}
        initial={agentInitial}
        whileHover={agentHover}
        whileTap={whileTap}
        onClick={onClick}
        {...props}
      >
        {/* Chinese character watermark */}
        <div
          className="absolute inset-0 flex items-center justify-center pointer-events-none select-none"
          style={{
            opacity: 0.1,
            transition: 'opacity 0.3s ease',
          }}
        >
          <span
            className="font-calligraphy text-[120px] text-ink-black"
            style={{ opacity: 0.1 }}
          >
            承
          </span>
        </div>
        {children}
      </motion.div>
    );
  }

  return (
    <motion.div
      className={`${baseStyles} ${className}`}
      initial={defaultInitial}
      whileHover={defaultHover}
      whileTap={whileTap}
      onClick={onClick}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default AnimatedCard;

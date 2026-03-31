import React from 'react';
import { motion } from 'framer-motion';

/**
 * Enhanced Button component with framer-motion, size variants, loading state, and icon slots.
 * Eastern aesthetic styling with vermilion accents.
 */
const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  iconLeft,
  iconRight,
  className = '',
  ...rest
}) => {
  const isDisabled = loading || disabled;

  // Base styles
  const baseStyles = 'font-xiaowei tracking-widest rounded-sm transition-all duration-200 inline-flex items-center justify-center gap-2';

  // Size classes
  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-8 py-3 text-lg',
    lg: 'px-12 py-4 text-xl',
  };

  // Variant classes
  const variantClasses = {
    primary: 'bg-ink-black text-rice-paper hover:bg-vermilion',
    outline: 'border border-ink-black/30 text-ink-black hover:border-ink-black hover:bg-ink-black/5',
    ghost: 'text-ink-black hover:text-vermilion',
  };

  // Icon size based on button size
  const iconSize = size === 'sm' ? '0.875em' : size === 'lg' ? '1.25em' : '1em';

  return (
    <motion.button
      className={`${baseStyles} ${sizeClasses[size]} ${variantClasses[variant]} ${isDisabled ? 'cursor-not-allowed opacity-60' : ''} ${className}`}
      disabled={isDisabled}
      whileHover={!isDisabled ? { scale: 1.02, y: -2 } : {}}
      whileTap={!isDisabled ? { scale: 0.97 } : {}}
      transition={{ duration: 0.15 }}
      {...rest}
    >
      {loading ? (
        <span className="inline-flex items-center gap-2">
          <span className="animate-pulse">处理中...</span>
        </span>
      ) : (
        <>
          {iconLeft && <span style={{ width: iconSize, height: iconSize, display: 'inline-flex' }}>{iconLeft}</span>}
          {children}
          {iconRight && <span style={{ width: iconSize, height: iconSize, display: 'inline-flex' }}>{iconRight}</span>}
        </>
      )}
    </motion.button>
  );
};

export default Button;

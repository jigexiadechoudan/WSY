/**
 * Design tokens for 数字传承人 (The Digital Inheritor)
 * Eastern aesthetics color palette, spacing, shadows, and animation values
 */

// Color tokens (matching tailwind.config.js)
export const inkBlack = '#2B2B2B';
export const ricePaper = '#F7F5F0';
export const vermilion = '#C04851';
export const cyanGlaze = '#5796B3';
export const teaGreen = '#CCD4BF';
export const charcoal = '#4A4A4A';

// Spacing tokens
export const spaceXs = '8px';
export const spaceSm = '16px';
export const spaceMd = '24px';
export const spaceLg = '40px';
export const spaceXl = '64px';

// Shadow depths
export const shadowSm = '0 2px 8px -2px rgba(43,43,43,0.1)';
export const shadowMd = '0 4px 20px -2px rgba(43,43,43,0.1)';
export const shadowLg = '0 12px 40px -4px rgba(43,43,43,0.2)';
export const shadowGlow = '0 0 20px rgba(192,72,81,0.15)';

// Animation durations
export const durationFast = '150ms';
export const durationNormal = '300ms';
export const durationSlow = '500ms';

// Easing curves
export const easeDefault = [0.4, 0, 0.2, 1];
export const easeIn = [0.4, 0, 1, 1];
export const easeOut = [0, 0, 0.2, 1];

// All tokens aggregated
export const tokens = {
  colors: {
    inkBlack,
    ricePaper,
    vermilion,
    cyanGlaze,
    teaGreen,
    charcoal,
  },
  spacing: {
    xs: spaceXs,
    sm: spaceSm,
    md: spaceMd,
    lg: spaceLg,
    xl: spaceXl,
  },
  shadows: {
    sm: shadowSm,
    md: shadowMd,
    lg: shadowLg,
    glow: shadowGlow,
  },
  durations: {
    fast: durationFast,
    normal: durationNormal,
    slow: durationSlow,
  },
  easing: {
    default: easeDefault,
    in: easeIn,
    out: easeOut,
  },
};

/* CSS Custom Properties template:
:root {
  --color-ink-black: #2B2B2B;
  --color-rice-paper: #F7F5F0;
  --color-vermilion: #C04851;
  --color-cyan-glaze: #5796B3;
  --color-tea-green: #CCD4BF;
  --color-charcoal: #4A4A4A;
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 24px;
  --space-lg: 40px;
  --space-xl: 64px;
  --shadow-sm: 0 2px 8px -2px rgba(43,43,43,0.1);
  --shadow-md: 0 4px 20px -2px rgba(43,43,43,0.1);
  --shadow-lg: 0 12px 40px -4px rgba(43,43,43,0.2);
  --shadow-glow: 0 0 20px rgba(192,72,81,0.15);
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
}
*/

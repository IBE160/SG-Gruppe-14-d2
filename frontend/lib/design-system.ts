/**
 * Design System - PM Simulator
 * Extracted from UX mockups: final-screen-02-dashboard-main.svg, final-screen-03-chat-interface.svg
 */

export const colors = {
  // Background colors
  background: {
    page: '#f9fafb',        // Main page background
    card: '#ffffff',        // Card/panel background
    input: '#f3f4f6',       // Input field background
  },

  // Budget tier colors
  budget: {
    tier1: {
      bg: '#eff6ff',        // Available budget background (blue)
      border: '#3b82f6',    // Available budget border
      text: '#1e40af',      // Available budget text
      progress: '#10b981',  // Green progress bar
    },
    tier2: {
      bg: '#f3f4f6',        // Locked budget background (gray)
      border: '#d1d5db',    // Locked budget border
      text: '#6b7280',      // Locked budget text
    },
    tier3: {
      bg: '#f9fafb',        // Total budget background
      border: '#d1d5db',    // Total budget border
    },
  },

  // Status colors
  status: {
    success: {
      bg: '#f0fdf4',        // Success background (green)
      border: '#10b981',    // Success border
      text: '#065f46',      // Success text dark
      textLight: '#047857', // Success text light
    },
    warning: {
      bg: '#fef3c7',        // Warning background (yellow)
      border: '#f59e0b',    // Warning border
      text: '#92400e',      // Warning text
    },
    error: {
      bg: '#fee2e2',        // Error background (red)
      border: '#ef4444',    // Error border
      text: '#991b1b',      // Error text dark
      textLight: '#7f1d1d', // Error text light
    },
  },

  // Chat colors
  chat: {
    user: {
      bg: '#eff6ff',        // User message background (blue)
      border: '#3b82f6',    // User message border
    },
    ai: {
      bg: '#f9fafb',        // AI message background (gray)
      border: '#d1d5db',    // AI message border
    },
    offer: {
      bg: '#f0fdf4',        // Offer box background (green)
      border: '#10b981',    // Offer box border (thick)
    },
  },

  // Button colors
  button: {
    primary: {
      bg: '#3b82f6',        // Primary button background (blue)
      text: '#ffffff',      // Primary button text
      hover: '#2563eb',     // Primary button hover
    },
    success: {
      bg: '#10b981',        // Success button background (green)
      text: '#ffffff',      // Success button text
      hover: '#059669',     // Success button hover
    },
    secondary: {
      bg: '#f3f4f6',        // Secondary button background (gray)
      border: '#d1d5db',    // Secondary button border
      text: '#374151',      // Secondary button text
    },
  },

  // Badge colors
  badge: {
    negotiable: {
      bg: '#dbeafe',        // Negotiable badge background (light blue)
      border: '#3b82f6',    // Negotiable badge border
      text: '#1e40af',      // Negotiable badge text
    },
    locked: {
      bg: '#e5e7eb',        // Locked badge background (gray)
      border: '#9ca3af',    // Locked badge border
      text: '#6b7280',      // Locked badge text
    },
  },

  // Text colors
  text: {
    primary: '#111827',     // Primary text (headings)
    secondary: '#374151',   // Secondary text (body)
    tertiary: '#6b7280',    // Tertiary text (descriptions)
    quaternary: '#9ca3af',  // Quaternary text (small text)
  },

  // Border colors
  border: {
    light: '#e5e7eb',       // Light border
    medium: '#d1d5db',      // Medium border
    dark: '#9ca3af',        // Dark border
  },

  // Agent colors
  agent: {
    owner: {
      bg: '#fef3c7',        // Owner agent background (yellow)
      border: '#f59e0b',    // Owner agent border
      text: '#92400e',      // Owner agent text
    },
    supplier: {
      bg: '#dbeafe',        // Supplier agent background (blue)
      border: '#3b82f6',    // Supplier agent border
      text: '#1e40af',      // Supplier agent text
    },
  },

  // WBS item colors
  wbs: {
    negotiable: {
      bg: '#eff6ff',        // Negotiable WBS background (blue)
      border: '#3b82f6',    // Negotiable WBS border (thick)
      leftBar: '#3b82f6',   // Left accent bar
      dot: '#3b82f6',       // Status dot
    },
    locked: {
      bg: '#f3f4f6',        // Locked WBS background (gray)
      border: '#d1d5db',    // Locked WBS border
      leftBar: '#9ca3af',   // Left accent bar
      text: '#6b7280',      // Text color
    },
  },
} as const;

export const typography = {
  fontFamily: {
    default: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  },

  fontSize: {
    // Dashboard sizes
    dashTitle: '20px',      // Main title
    dashHeading: '16px',    // Section headings
    dashText: '13px',       // Body text
    dashDesc: '11px',       // Description text
    dashSmall: '10px',      // Small text
    dashBadge: '10px',      // Badge text

    // Chat sizes
    chatTitle: '18px',      // Chat title
    chatSubtitle: '14px',   // Chat subtitle
    chatText: '13px',       // Chat body text
    chatDesc: '12px',       // Chat description
    chatSmall: '11px',      // Chat small text
    chatBtnText: '13px',    // Chat button text
  },

  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },

  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const;

export const spacing = {
  // Padding
  p1: '4px',
  p2: '8px',
  p3: '12px',
  p4: '16px',
  p5: '20px',
  p6: '24px',
  p8: '32px',

  // Margin
  m1: '4px',
  m2: '8px',
  m3: '12px',
  m4: '16px',
  m5: '20px',
  m6: '24px',
  m8: '32px',

  // Gap
  gap2: '8px',
  gap4: '16px',
  gap6: '24px',
} as const;

export const borderRadius = {
  sm: '4px',
  md: '6px',
  lg: '8px',
  xl: '10px',
  full: '9999px',
} as const;

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
} as const;

// Helper function to get progress bar color based on percentage
export function getBudgetProgressColor(percentage: number): string {
  if (percentage > 100) return colors.status.error.border; // Red
  if (percentage > 90) return colors.status.warning.border; // Yellow
  if (percentage > 70) return colors.status.warning.border; // Yellow
  return colors.budget.tier1.progress; // Green
}

// Helper function to get status badge color
export function getStatusColor(status: 'pending' | 'in_progress' | 'completed' | 'rejected'): string {
  switch (status) {
    case 'completed':
      return colors.status.success.border;
    case 'in_progress':
      return colors.button.primary.bg;
    case 'rejected':
      return colors.status.error.border;
    default:
      return colors.text.quaternary;
  }
}

// Export all as default
export default {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  getBudgetProgressColor,
  getStatusColor,
};

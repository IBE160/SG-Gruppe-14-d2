/**
 * Shared timeline calculation utility
 * Used by both Gantt Chart and Precedence Diagram
 *
 * Calculates ES/EF/LS/LF based on:
 * - WBS dependencies
 * - Committed durations (accepted contracts)
 * - Locked durations (pre-negotiated items)
 * - Baseline durations (negotiable items not yet committed)
 */

export interface TimelineData {
  es: Record<string, number>;        // Earliest Start (days from project start)
  ef: Record<string, number>;        // Earliest Finish (days from project start)
  ls: Record<string, number>;        // Latest Start (days from project start)
  lf: Record<string, number>;        // Latest Finish (days from project start)
  slack: Record<string, number>;     // Total Float/Slack (days)
  projectEnd: number;                // Project end date (days from start)
}

interface WBSItem {
  id: string;
  dependencies: string[];
  is_negotiable: boolean;
  baseline_duration?: number;
  locked_duration?: number;
  critical_path?: boolean;
}

interface Commitment {
  wbs_id?: string;
  wbs_item_id?: string;
  committed_duration?: number;
  committed_cost?: number;
}

/**
 * Get the effective duration for a WBS item
 * Priority: committed_duration > locked_duration > baseline_duration
 */
function getEffectiveDuration(
  item: WBSItem,
  commitments: Commitment[]
): number {
  // Check if there's a commitment for this item
  const commitment = commitments.find(
    c => c.wbs_id === item.id || c.wbs_item_id === item.id
  );

  if (commitment?.committed_duration) {
    return commitment.committed_duration;
  }

  // Use locked_duration for non-negotiable items
  if (!item.is_negotiable && item.locked_duration) {
    return item.locked_duration;
  }

  // Use baseline_duration for negotiable items
  if (item.is_negotiable && item.baseline_duration) {
    return item.baseline_duration;
  }

  // Fallback default
  return 30;
}

/**
 * Calculate timeline data using CPM (Critical Path Method)
 */
export function calculateTimeline(
  wbsItems: WBSItem[],
  commitments: Commitment[] = []
): TimelineData {
  const es: Record<string, number> = {};
  const ef: Record<string, number> = {};
  const ls: Record<string, number> = {};
  const lf: Record<string, number> = {};
  const slack: Record<string, number> = {};

  // FORWARD PASS: Calculate ES and EF
  const calculateForward = (
    itemId: string,
    visited = new Set<string>()
  ): number => {
    // Already calculated
    if (ef[itemId] !== undefined) return ef[itemId];

    // Circular dependency detection
    if (visited.has(itemId)) {
      console.warn(`Circular dependency detected for ${itemId}`);
      return 0;
    }

    visited.add(itemId);

    const item = wbsItems.find(w => w.id === itemId);
    if (!item) {
      console.warn(`WBS item ${itemId} not found`);
      return 0;
    }

    const duration = getEffectiveDuration(item, commitments);

    // ES = max(EF of all predecessors)
    let maxPredecessorEF = 0;
    const dependencies = item.dependencies || [];

    dependencies.forEach((depId: string) => {
      const depEF = calculateForward(depId, new Set(visited));
      if (depEF > maxPredecessorEF) {
        maxPredecessorEF = depEF;
      }
    });

    es[itemId] = maxPredecessorEF;
    ef[itemId] = es[itemId] + duration;

    return ef[itemId];
  };

  // Calculate forward pass for all items
  wbsItems.forEach(item => {
    calculateForward(item.id);
  });

  // Find project end date (max EF across all items)
  const projectEnd = Math.max(...Object.values(ef), 0);

  // BACKWARD PASS: Calculate LS and LF
  const calculateBackward = (
    itemId: string,
    visited = new Set<string>()
  ): number => {
    // Already calculated
    if (ls[itemId] !== undefined) return ls[itemId];

    // Circular dependency detection
    if (visited.has(itemId)) {
      console.warn(`Circular dependency detected in backward pass for ${itemId}`);
      return projectEnd;
    }

    visited.add(itemId);

    const item = wbsItems.find(w => w.id === itemId);
    if (!item) {
      console.warn(`WBS item ${itemId} not found`);
      return projectEnd;
    }

    const duration = getEffectiveDuration(item, commitments);

    // Find all successors (items that depend on this item)
    const successors = wbsItems.filter(w =>
      (w.dependencies || []).includes(itemId)
    );

    if (successors.length === 0) {
      // No successors: this is an end node
      lf[itemId] = projectEnd;
      ls[itemId] = lf[itemId] - duration;
    } else {
      // LF = min(LS of all successors)
      let minSuccessorLS = projectEnd;

      successors.forEach(succ => {
        const succLS = calculateBackward(succ.id, new Set(visited));
        if (succLS < minSuccessorLS) {
          minSuccessorLS = succLS;
        }
      });

      lf[itemId] = minSuccessorLS;
      ls[itemId] = lf[itemId] - duration;
    }

    return ls[itemId];
  };

  // Calculate backward pass for all items
  wbsItems.forEach(item => {
    calculateBackward(item.id);
  });

  // Calculate slack for all items
  wbsItems.forEach(item => {
    slack[item.id] = ls[item.id] - es[item.id];
  });

  return {
    es,
    ef,
    ls,
    lf,
    slack,
    projectEnd
  };
}

/**
 * Convert day numbers to actual dates
 */
export function daysToDate(days: number, projectStart: Date): Date {
  const date = new Date(projectStart);
  date.setDate(date.getDate() + days);
  return date;
}

/**
 * Convert dates to day numbers
 */
export function dateToDays(date: Date, projectStart: Date): number {
  return Math.ceil(
    (date.getTime() - projectStart.getTime()) / (1000 * 60 * 60 * 24)
  );
}

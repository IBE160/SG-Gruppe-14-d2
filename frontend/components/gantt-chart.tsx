"use client";

import { useMemo, useEffect } from 'react';
import { Gantt, Task, ViewMode } from 'gantt-task-react';
import 'gantt-task-react/dist/index.css';
import '@/styles/gantt-override.css';
import { calculateTimeline, daysToDate } from '@/lib/timeline-calculator';

interface GanttChartProps {
  wbsItems: any[];
  commitments: any[];
  timeline: any; // from validation endpoint
}

export function GanttChart({ wbsItems, commitments, timeline }: GanttChartProps) {
  const projectStart = new Date('2025-01-15');

  // Calculate timeline data using shared utility
  const timelineData = useMemo(() => {
    const hasBackendData = timeline?.earliest_start && Object.keys(timeline.earliest_start).length > 0;

    if (hasBackendData) {
      return {
        earliestStart: timeline.earliest_start,
        earliestFinish: timeline.earliest_finish
      };
    }

    // Fallback: Calculate using shared utility
    const calculated = calculateTimeline(wbsItems, commitments);

    // Convert day numbers to dates
    const earliestStart: Record<string, string> = {};
    const earliestFinish: Record<string, string> = {};

    Object.keys(calculated.es).forEach(id => {
      earliestStart[id] = daysToDate(calculated.es[id], projectStart).toISOString();
      earliestFinish[id] = daysToDate(calculated.ef[id], projectStart).toISOString();
    });

    return { earliestStart, earliestFinish };
  }, [wbsItems, commitments, timeline]);

  const tasks: Task[] = useMemo(() => {
    const commitmentMap = Object.fromEntries(
      commitments.map((c: any) => [c.wbs_id || c.wbs_item_id, c])
    );

    return wbsItems
      .map((item) => {
        const commitment = commitmentMap[item.id];

        // Get dates from timelineData (either backend or calculated)
        let start: Date;
        let end: Date;

        if (timelineData.earliestStart[item.id] && timelineData.earliestFinish[item.id]) {
          start = new Date(timelineData.earliestStart[item.id]);
          end = new Date(timelineData.earliestFinish[item.id]);
        } else {
          // Fallback: use project start + duration
          const duration = item.is_negotiable
            ? (item.baseline_duration || 30)
            : (item.locked_duration || 30);
          start = projectStart;
          end = new Date(projectStart.getTime() + duration * 24 * 60 * 60 * 1000);
        }

        // Critical path comes from the WBS item itself, not backend
        const isCritical = item.critical_path === true;
        const isCommitted = !!commitment;
        const isNegotiable = item.is_negotiable;

        // Color based on status (not critical path)
        let backgroundColor, backgroundSelectedColor, progressColor, progressSelectedColor;

        if (isCommitted || !isNegotiable) {
          // Committed or locked = GREY
          backgroundColor = '#9ca3af';
          backgroundSelectedColor = '#6b7280';
          progressColor = '#4b5563';
          progressSelectedColor = '#374151';
        } else {
          // Negotiable = BLUE
          backgroundColor = '#60a5fa';
          backgroundSelectedColor = '#3b82f6';
          progressColor = '#2563eb';
          progressSelectedColor = '#1d4ed8';
        }

        const barStyle = {
          backgroundColor,
          backgroundSelectedColor,
          progressColor,
          progressSelectedColor,
        };

        return {
          id: item.id,
          name: `${item.id} - ${item.name}`,
          start,
          end,
          progress: isCommitted ? 100 : 0,
          type: 'task' as const,
          styles: barStyle,
          dependencies: item.dependencies || []
        } as Task;
      })
      .filter((task): task is Task => task !== null);
  }, [wbsItems, commitments, timelineData]);

  // Add red outline to critical path items after render
  useEffect(() => {
    // Critical path WBS IDs (from wbs.json)
    const criticalIds = new Set(['1.3.1', '1.3.2', '1.4.1', '1.1.1', '1.2.1', '1.9.1']);

    // Wait for SVG to render
    setTimeout(() => {
      const container = document.querySelector('.gantt-container');
      if (!container) return;

      console.log('🔴 CRITICAL PATH OUTLINING STARTED');

      // Find all task bar rects (with fill colors and reasonable width)
      // Exclude the "today" indicator which has rgba(59, 130, 246, 0.3) fill
      const allRects = Array.from(container.querySelectorAll('svg rect'))
        .filter((rect: any) => {
          const fill = rect.getAttribute('fill');
          const width = parseFloat(rect.getAttribute('width') || '0');
          const y = parseFloat(rect.getAttribute('y') || '0');

          // Filter out the "today" indicator (Y=0, semi-transparent blue)
          if (y === 0 && fill?.includes('rgba')) {
            return false;
          }

          return fill && fill !== 'none' && width > 10;
        });

      console.log(`📊 Found ${allRects.length} task bar rects for ${tasks.length} tasks`);
      console.log(`📊 Ratio: ${(allRects.length / tasks.length).toFixed(2)} rects per task`);

      // Log first 3 rects' Y coordinates to understand the pattern
      console.log('📍 Sample Y coordinates:');
      allRects.slice(0, 6).forEach((rect: any, i) => {
        const y = rect.getAttribute('y');
        const fill = rect.getAttribute('fill');
        console.log(`  Rect ${i}: Y=${y}, fill=${fill}`);
      });

      // Log task order with indices
      console.log('📋 Tasks order:');
      tasks.forEach((task, i) => {
        const critical = criticalIds.has(task.id) ? '🔴 CRITICAL' : '⚪';
        console.log(`  ${i}: ${task.id} ${critical}`);
      });

      // Find critical task indices
      const criticalIndices = tasks
        .map((task, index) => criticalIds.has(task.id) ? index : -1)
        .filter(index => index !== -1);

      console.log(`🎯 Critical task indices: [${criticalIndices.join(', ')}]`);

      // Assume 2 rects per task (background + progress) and outline accordingly
      const rectsPerTask = Math.round(allRects.length / tasks.length);
      console.log(`🎯 Using ${rectsPerTask} rects per task for matching`);

      criticalIndices.forEach(taskIdx => {
        const startRect = taskIdx * rectsPerTask;
        const endRect = startRect + rectsPerTask;

        console.log(`🎯 Task ${taskIdx} (${tasks[taskIdx].id}): outlining rects ${startRect}-${endRect - 1}`);

        for (let i = startRect; i < endRect && i < allRects.length; i++) {
          const rect = allRects[i] as any;
          rect.style.stroke = '#dc2626';
          rect.style.strokeWidth = '2px';
        }
      });

      console.log('🔴 CRITICAL PATH OUTLINING COMPLETED');
    }, 500);
  }, [tasks]);

  // Set Norwegian locale and Month view by default
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
      <h3 className="text-xl font-bold mb-4">Gantt-diagram</h3>

      <div className="gantt-container" style={{ width: '100%', overflowX: 'auto' }}>
        <style dangerouslySetInnerHTML={{__html: `
          /* Force everything */

          /* ALL text BLACK */
          .gantt-container * {
            color: #000000 !important;
          }

          /* Override ANY background to grey */
          .gantt-container div[style],
          .gantt-container div[style*="background"],
          .gantt-container div[style*="color"] {
            background-color: #d1d5db !important;
            color: #000000 !important;
          }

          /* Force all children too */
          .gantt-container div[style] *,
          .gantt-container div[style*="background"] *,
          .gantt-container div[style*="color"] * {
            color: #000000 !important;
          }

          /* BRUTE FORCE: Make first child of gantt container bigger and bold */
          .gantt-container > div:nth-child(1),
          .gantt-container > div:nth-child(1) div,
          .gantt-container > div:nth-child(1) span {
            font-size: 15px !important;
            font-weight: 700 !important;
          }

          /* Make table columns narrower and auto-width */
          .gantt-container [class*="taskList"] {
            min-width: auto !important;
            width: auto !important;
          }

          /* Show bar labels with white text - smaller */
          .gantt-container svg text {
            display: block !important;
            fill: #ffffff !important;
            font-size: 9px !important;
            font-weight: 600 !important;
          }

          /* Make grid lines very light grey (almost invisible) */
          .gantt-container svg line {
            stroke: #f3f4f6 !important;
            stroke-opacity: 0.3 !important;
          }

          /* Critical path outline - DISABLED for now */
          /* Will be added via different method */

          /* When text overflows, make it dark and position outside */
          .gantt-container svg g[class*="bar"] text[x] {
            fill: #1f2937 !important;
          }

          /* Keep bar labels white by default */
          .gantt-container svg g[aria-label] text {
            fill: #ffffff !important;
          }

          /* Keep calendar/grid text black */
          .gantt-container svg g[class*="calendar"] text,
          .gantt-container svg g[class*="grid"] text,
          .gantt-container svg g[class*="Calendar"] text,
          .gantt-container svg g[class*="Grid"] text {
            fill: #000000 !important;
          }
        `}} />
        <Gantt
          tasks={tasks}
          viewMode={ViewMode.Month}
          locale="nb-NO"
          listCellWidth="180px"
          columnWidth={70}
          barProgressColor="#3b82f6"
          barBackgroundColor="#e5e7eb"
          todayColor="rgba(59, 130, 246, 0.3)"
          fontSize="9px"
          fontFamily="Inter, system-ui, sans-serif"
        />
      </div>

      {/* Legend */}
      <div className="mt-6 flex gap-4 text-sm flex-wrap">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-blue-400 rounded"></div>
          <span>Kan forhandles</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-gray-400 rounded"></div>
          <span>Forpliktet/låst</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-red-600 rounded bg-transparent"></div>
          <span>Kritisk sti (rød outline)</span>
        </div>
      </div>
    </div>
  );
}

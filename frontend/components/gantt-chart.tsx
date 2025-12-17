"use client";

import { useMemo } from 'react';
import { Gantt, Task, ViewMode } from 'gantt-task-react';
import 'gantt-task-react/dist/index.css';

interface GanttChartProps {
  wbsItems: any[];
  commitments: any[];
  timeline: any; // from validation endpoint
}

export function GanttChart({ wbsItems, commitments, timeline }: GanttChartProps) {
  const tasks: Task[] = useMemo(() => {
    const commitmentMap = Object.fromEntries(
      commitments.map((c: any) => [c.wbs_id, c])
    );

    const earliestStart = timeline?.earliest_start || {};
    const earliestFinish = timeline?.earliest_finish || {};
    const criticalPath = timeline?.critical_path || [];

    return wbsItems
      .map((item) => {
        const commitment = commitmentMap[item.id];
        const start = earliestStart[item.id] ? new Date(earliestStart[item.id]) : null;
        const end = earliestFinish[item.id] ? new Date(earliestFinish[item.id]) : null;

        if (!start || !end) return null;

        const isCritical = criticalPath.includes(item.id);
        const isCommitted = !!commitment;
        const isNegotiable = item.is_negotiable;

        // Color priority: Critical path (RED) > Committed (GREEN) > Negotiable (BLUE) > Locked (GREY)
        let backgroundColor = '#9ca3af'; // Default: Grey for locked items
        let backgroundSelectedColor = '#6b7280';
        let progressColor = '#4b5563';
        let progressSelectedColor = '#374151';

        if (isCritical) {
          // Critical path items are RED (highest priority)
          backgroundColor = '#ef4444';
          backgroundSelectedColor = '#dc2626';
          progressColor = '#991b1b';
          progressSelectedColor = '#7f1d1d';
        } else if (isCommitted) {
          // Committed items are GREEN (contract accepted)
          backgroundColor = '#22c55e';
          backgroundSelectedColor = '#16a34a';
          progressColor = '#15803d';
          progressSelectedColor = '#14532d';
        } else if (isNegotiable) {
          // Negotiable items (not yet committed) are LIGHT BLUE
          backgroundColor = '#60a5fa';
          backgroundSelectedColor = '#3b82f6';
          progressColor = '#2563eb';
          progressSelectedColor = '#1d4ed8';
        }

        return {
          id: item.id,
          name: `${item.id} - ${item.name}`,
          start,
          end,
          progress: isCommitted ? 100 : 0,
          type: 'task' as const,
          styles: {
            backgroundColor,
            backgroundSelectedColor,
            progressColor,
            progressSelectedColor
          },
          dependencies: item.dependencies || []
        } as Task;
      })
      .filter((task): task is Task => task !== null);
  }, [wbsItems, commitments, timeline]);

  if (tasks.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-bold mb-4">Gantt-diagram</h3>
        <p className="text-sm text-gray-600">
          Ingen oppgaver å vise. Vennligst forplikte deg til minst én arbeidspakke.
        </p>
      </div>
    );
  }

  // Set Norwegian locale and Month view by default
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
      <h3 className="text-xl font-bold mb-4">Gantt-diagram</h3>

      <div className="gantt-wrapper" style={{ width: '100%', overflowX: 'auto' }}>
        <Gantt
          tasks={tasks}
          viewMode={ViewMode.Month}
          locale="nb-NO"
          listCellWidth="200px"
          columnWidth={60}
          barProgressColor="#3b82f6"
          barBackgroundColor="#e5e7eb"
          todayColor="rgba(59, 130, 246, 0.3)"
        />
      </div>

      {/* Legend */}
      <div className="mt-6 flex gap-4 text-sm flex-wrap">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-red-500 rounded"></div>
          <span>Kritisk sti</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-green-500 rounded"></div>
          <span>Kontraktfestet</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-blue-400 rounded"></div>
          <span>Kan forhandles</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 bg-gray-400 rounded"></div>
          <span>Låst (ikke forhandlingsbar)</span>
        </div>
      </div>
    </div>
  );
}

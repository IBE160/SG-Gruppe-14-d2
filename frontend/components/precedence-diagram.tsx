"use client";

import { useMemo } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  BackgroundVariant
} from 'reactflow';
import 'reactflow/dist/style.css';

interface PrecedenceDiagramProps {
  wbsItems: any[];
  timeline: any;
}

export function PrecedenceDiagram({ wbsItems, timeline }: PrecedenceDiagramProps) {
  const criticalPath = timeline?.critical_path || [];
  const earliestStart = timeline?.earliest_start || {};
  const earliestFinish = timeline?.earliest_finish || {};
  const latestStart = timeline?.latest_start || {};
  const latestFinish = timeline?.latest_finish || {};
  const slack = timeline?.slack || {};

  const initialNodes: Node[] = useMemo(() => {
    return wbsItems.map((item, idx) => {
      const es = earliestStart[item.id]
        ? Math.ceil((new Date(earliestStart[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0;
      const ef = earliestFinish[item.id]
        ? Math.ceil((new Date(earliestFinish[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0;
      const ls = latestStart[item.id]
        ? Math.ceil((new Date(latestStart[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0;
      const lf = latestFinish[item.id]
        ? Math.ceil((new Date(latestFinish[item.id]).getTime() - new Date('2025-01-15').getTime()) / (1000 * 60 * 60 * 24))
        : 0;
      const taskSlack = slack[item.id] ?? 0;
      const isCritical = criticalPath.includes(item.id);

      return {
        id: item.id,
        type: 'default',
        position: { x: (idx % 5) * 220 + 50, y: Math.floor(idx / 5) * 180 + 50 },
        data: {
          label: (
            <div className="text-center p-2">
              <div className="font-bold text-sm mb-1">{item.id}</div>
              <div className="text-xs mb-1 text-gray-700">
                {item.name.length > 20 ? item.name.substring(0, 20) + '...' : item.name}
              </div>
              <div className="text-xs text-gray-600 mt-2">
                <div>ES: {es} | EF: {ef}</div>
                <div>LS: {ls} | LF: {lf}</div>
              </div>
              <div className={`text-xs font-semibold mt-1 ${taskSlack === 0 ? 'text-red-600' : 'text-green-600'}`}>
                {taskSlack === 0 ? 'KRITISK' : `Slack: ${taskSlack}d`}
              </div>
            </div>
          )
        },
        style: {
          background: isCritical ? '#fee2e2' : '#f3f4f6',
          border: `${isCritical ? '3' : '2'}px solid ${isCritical ? '#ef4444' : '#9ca3af'}`,
          borderRadius: '8px',
          width: 180,
          fontSize: '12px'
        }
      };
    });
  }, [wbsItems, timeline]);

  const initialEdges: Edge[] = useMemo(() => {
    const edges: Edge[] = [];
    wbsItems.forEach((item) => {
      const dependencies = item.dependencies || [];
      dependencies.forEach((depId: string) => {
        const isCritical =
          criticalPath.includes(item.id) && criticalPath.includes(depId);

        edges.push({
          id: `${depId}-${item.id}`,
          source: depId,
          target: item.id,
          type: 'smoothstep',
          animated: isCritical,
          style: {
            stroke: isCritical ? '#ef4444' : '#9ca3af',
            strokeWidth: isCritical ? 3 : 2
          },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            color: isCritical ? '#ef4444' : '#9ca3af'
          }
        });
      });
    });
    return edges;
  }, [wbsItems, timeline]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  if (wbsItems.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
        <h3 className="text-xl font-bold mb-4">Presedensdiagram (AON)</h3>
        <p className="text-sm text-gray-600">
          Ingen oppgaver å vise. Vennligst forplikte deg til minst én arbeidspakke.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
      <h3 className="text-xl font-bold mb-4">Presedensdiagram (AON)</h3>

      <div style={{ width: '100%', height: '600px' }} className="border border-gray-200 dark:border-gray-700 rounded">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          attributionPosition="bottom-left"
        >
          <Background variant={BackgroundVariant.Dots} />
          <Controls />
        </ReactFlow>
      </div>

      {/* Legend */}
      <div className="mt-4 flex gap-4 text-sm flex-wrap">
        <div className="flex items-center gap-2">
          <div className="w-12 h-8 bg-red-100 border-2 border-red-500 rounded"></div>
          <span>Kritisk sti</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-12 h-8 bg-gray-100 border-2 border-gray-400 rounded"></div>
          <span>Ikke-kritisk</span>
        </div>
        <div className="text-xs text-gray-700">
          <strong>ES</strong>=Tidligst start, <strong>EF</strong>=Tidligst slutt,
          <strong> LS</strong>=Senest start, <strong>LF</strong>=Senest slutt
        </div>
      </div>
    </div>
  );
}

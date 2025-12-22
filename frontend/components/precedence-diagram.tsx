"use client";

import { useMemo, useEffect, useCallback } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  BackgroundVariant,
  NodeChange
} from 'reactflow';
import 'reactflow/dist/style.css';
import { calculateTimeline, dateToDays } from '@/lib/timeline-calculator';

interface PrecedenceDiagramProps {
  wbsItems: any[];
  commitments: any[];
  timeline: any;
}

const STORAGE_KEY = 'precedence-diagram-layout';

export function PrecedenceDiagram({ wbsItems, commitments, timeline }: PrecedenceDiagramProps) {
  // Calculate timeline data (ES/EF/LS/LF)
  const timelineData = useMemo(() => {
    // Try to use backend timeline data first
    const hasBackendData = timeline?.earliest_start && Object.keys(timeline.earliest_start).length > 0;

    if (hasBackendData) {
      // Convert backend dates to day numbers
      const projectStart = new Date('2025-01-15');
      const es: Record<string, number> = {};
      const ef: Record<string, number> = {};
      const ls: Record<string, number> = {};
      const lf: Record<string, number> = {};

      Object.keys(timeline.earliest_start).forEach(id => {
        es[id] = dateToDays(new Date(timeline.earliest_start[id]), projectStart);
        ef[id] = dateToDays(new Date(timeline.earliest_finish[id]), projectStart);
        ls[id] = dateToDays(new Date(timeline.latest_start[id]), projectStart);
        lf[id] = dateToDays(new Date(timeline.latest_finish[id]), projectStart);
      });

      return {
        es,
        ef,
        ls,
        lf,
        slack: timeline.slack || {},
        projectEnd: Math.max(...Object.values(ef))
      };
    }

    // Fallback: Calculate locally using shared utility
    return calculateTimeline(wbsItems, commitments);
  }, [wbsItems, commitments, timeline]);

  // Function to calculate default grid positions
  const getDefaultPosition = useCallback((idx: number) => ({
    x: (idx % 5) * 220 + 50,
    y: Math.floor(idx / 5) * 180 + 50
  }), []);

  const initialNodes: Node[] = useMemo(() => {
    // Load saved positions from localStorage
    let savedPositions: Record<string, { x: number; y: number }> = {};
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        savedPositions = JSON.parse(saved);
      }
    } catch (error) {
      console.warn('Failed to load saved layout:', error);
    }

    return wbsItems.map((item, idx) => {
      const es = timelineData.es[item.id] || 0;
      const ef = timelineData.ef[item.id] || 0;
      const ls = timelineData.ls[item.id] || 0;
      const lf = timelineData.lf[item.id] || 0;
      const taskSlack = timelineData.slack[item.id] || 0;

      // Critical path designation ALWAYS from wbs.json (not calculated)
      const isCritical = item.critical_path === true;

      // Use saved position if available, otherwise use default grid layout
      const position = savedPositions[item.id] || getDefaultPosition(idx);

      return {
        id: item.id,
        type: 'default',
        position,
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
              <div className={`text-xs font-semibold mt-1 ${isCritical ? 'text-red-600' : 'text-green-600'}`}>
                {isCritical ? 'KRITISK' : `Slack: ${taskSlack}d`}
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
  }, [wbsItems, timelineData]);

  const initialEdges: Edge[] = useMemo(() => {
    const edges: Edge[] = [];
    wbsItems.forEach((item) => {
      const dependencies = item.dependencies || [];
      const targetItem = wbsItems.find(w => w.id === item.id);
      const isTargetCritical = targetItem?.critical_path === true;

      dependencies.forEach((depId: string) => {
        const sourceItem = wbsItems.find(w => w.id === depId);
        const isSourceCritical = sourceItem?.critical_path === true;

        // Edge is critical only if both source and target are on critical path
        const isCritical = isSourceCritical && isTargetCritical;

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
  }, [wbsItems, timelineData]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // Save node positions to localStorage when they change
  const handleNodesChange = useCallback((changes: NodeChange[]) => {
    onNodesChange(changes);

    // Save positions after nodes are moved
    const hasPositionChange = changes.some(
      change => change.type === 'position' && change.dragging === false
    );

    if (hasPositionChange) {
      // Get current node positions
      const positions: Record<string, { x: number; y: number }> = {};
      nodes.forEach(node => {
        positions[node.id] = { x: node.position.x, y: node.position.y };
      });

      // Save to localStorage
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(positions));
        console.log('💾 Saved diagram layout');
      } catch (error) {
        console.warn('Failed to save layout:', error);
      }
    }
  }, [nodes, onNodesChange]);

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

  // Reset layout to default positions
  const resetLayout = useCallback(() => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      console.log('🔄 Reset diagram layout');

      // Reset all nodes to default grid positions
      const resetNodes = nodes.map((node, idx) => ({
        ...node,
        position: getDefaultPosition(idx)
      }));

      setNodes(resetNodes);
    } catch (error) {
      console.warn('Failed to reset layout:', error);
    }
  }, [nodes, setNodes, getDefaultPosition]);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-bold">Presedensdiagram (AON)</h3>
        <button
          onClick={resetLayout}
          className="px-3 py-1 text-sm bg-gray-200 hover:bg-gray-300 rounded transition-colors"
          title="Tilbakestill layout til standard"
        >
          🔄 Tilbakestill layout
        </button>
      </div>

      <div style={{ width: '100%', height: '600px' }} className="border border-gray-200 dark:border-gray-700 rounded">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={handleNodesChange}
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

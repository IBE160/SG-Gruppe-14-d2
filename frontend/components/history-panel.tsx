"use client";

import { useEffect, useState } from 'react';
import { colors } from '@/lib/design-system';
import { getAuthToken } from '@/lib/auth-utils';
import { GanttChart } from './gantt-chart';
import { PrecedenceDiagram } from './precedence-diagram';

interface Snapshot {
  id: string;
  session_id: string;
  version: number;
  label: string;
  snapshot_type: string;
  budget_committed: number;
  budget_available: number;
  budget_total: number;
  contract_wbs_id: string | null;
  contract_cost: number | null;
  contract_duration: number | null;
  contract_supplier: string | null;
  project_end_date: string;
  days_before_deadline: number;
  gantt_state: any;
  precedence_state: any;
  timestamp: string;
  created_at: string;
}

interface HistoryPanelProps {
  sessionId: string;
  isOpen: boolean;
  onClose: () => void;
  wbsItems: any[];
}

export function HistoryPanel({ sessionId, isOpen, onClose, wbsItems }: HistoryPanelProps) {
  const [snapshots, setSnapshots] = useState<Snapshot[]>([]);
  const [selectedSnapshot, setSelectedSnapshot] = useState<Snapshot | null>(null);
  const [totalCount, setTotalCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMore, setHasMore] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'gantt' | 'precedence'>('overview');

  useEffect(() => {
    if (isOpen && sessionId) {
      loadSnapshots(0, 5);
    }
  }, [isOpen, sessionId]);

  async function loadSnapshots(offset: number, limit: number) {
    setIsLoading(true);
    try {
      const token = await getAuthToken();
      if (!token) {
        console.error('No auth token found');
        return;
      }

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${sessionId}/snapshots?limit=${limit}&offset=${offset}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Snapshot load failed:', response.status, errorText);
        throw new Error(`Failed to load snapshots: ${response.status} - ${errorText}`);
      }

      const data = await response.json();

      if (offset === 0) {
        setSnapshots(data.snapshots);
        if (data.snapshots.length > 0) {
          setSelectedSnapshot(data.snapshots[0]);
        }
      } else {
        setSnapshots(prev => [...prev, ...data.snapshots]);
      }

      setTotalCount(data.total_count);
      setHasMore(data.has_more);
    } catch (error) {
      console.error('Error loading snapshots:', error);
    } finally {
      setIsLoading(false);
    }
  }

  function loadMoreSnapshots() {
    if (!isLoading && hasMore) {
      loadSnapshots(snapshots.length, 10);
    }
  }

  async function exportHistory() {
    try {
      const token = await getAuthToken();
      if (!token) return;

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/sessions/${sessionId}/snapshots/export`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Export failed:', response.status, errorText);
        throw new Error(`Export failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `history-${sessionId}-${new Date().toISOString()}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting history:', error);
    }
  }

  if (!isOpen) return null;

  const formatBudget = (oreAmount: number) => {
    return (oreAmount / 100 / 1_000_000).toFixed(0);
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('nb-NO', { day: 'numeric', month: 'short', year: 'numeric' });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div
        className="relative mx-4 h-[90vh] w-full max-w-7xl overflow-hidden rounded-lg"
        style={{ backgroundColor: colors.background.card }}
      >
        {/* Header */}
        <div
          className="flex items-center justify-between border-b px-6 py-4"
          style={{ borderColor: colors.border.medium, backgroundColor: colors.background.input }}
        >
          <div>
            <h2 className="text-xl font-bold text-gray-900">🕒 Historikk - Kontrakt Aksepteringer</h2>
            <p className="text-sm text-gray-600">
              {totalCount} snapshot{totalCount !== 1 ? 's' : ''} lagret
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-2xl font-bold text-red-600 hover:text-red-700"
          >
            ✕
          </button>
        </div>

        <div className="flex h-[calc(100%-72px)]">
          {/* Left Sidebar - Timeline */}
          <div
            className="w-96 overflow-y-auto border-r"
            style={{ borderColor: colors.border.medium, backgroundColor: colors.background.input }}
          >
            <div className="p-4">
              <div className="mb-4">
                <select
                  className="w-full rounded border px-3 py-2 text-sm"
                  style={{ borderColor: colors.border.medium }}
                >
                  <option>Filter: Alle kontrakter ▼</option>
                </select>
              </div>

              {/* Timeline */}
              <div className="space-y-3">
                {snapshots.map((snapshot, index) => {
                  const isSelected = selectedSnapshot?.id === snapshot.id;
                  const isBaseline = snapshot.snapshot_type === 'baseline';

                  return (
                    <div
                      key={snapshot.id}
                      onClick={() => setSelectedSnapshot(snapshot)}
                      className={`cursor-pointer rounded-lg border-2 p-4 transition-all ${
                        isSelected ? 'shadow-md' : ''
                      }`}
                      style={{
                        backgroundColor: isSelected ? colors.budget.tier1.bg : colors.background.card,
                        borderColor: isSelected ? colors.button.primary.bg : colors.border.light,
                      }}
                    >
                      <div className="mb-2 flex items-center gap-2">
                        <span
                          className="rounded px-2 py-1 text-xs font-semibold text-white"
                          style={{
                            backgroundColor: isBaseline ? colors.button.primary.bg : colors.status.success.border,
                          }}
                        >
                          Versjon {snapshot.version}
                        </span>
                      </div>
                      <h3 className="text-sm font-semibold text-gray-900">{snapshot.label}</h3>
                      {snapshot.contract_wbs_id && (
                        <p className="mt-1 text-xs text-gray-700">
                          ✓ WBS {snapshot.contract_wbs_id} - {snapshot.contract_supplier}
                        </p>
                      )}
                      {snapshot.contract_cost && (
                        <p className="mt-1 text-xs text-gray-600">
                          • {formatBudget(snapshot.contract_cost)} MNOK, {snapshot.contract_duration} dager
                        </p>
                      )}
                      <p className="mt-2 text-xs text-gray-500">
                        {formatDate(snapshot.created_at)}
                      </p>
                    </div>
                  );
                })}

                {/* Load More Button */}
                {hasMore && (
                  <button
                    onClick={loadMoreSnapshots}
                    disabled={isLoading}
                    className="w-full rounded border px-4 py-2 text-sm font-semibold transition-colors"
                    style={{
                      borderColor: colors.border.medium,
                      backgroundColor: colors.background.card,
                    }}
                  >
                    {isLoading ? 'Laster...' : 'Last flere ↓'}
                  </button>
                )}

                {/* Count */}
                <p className="text-center text-xs text-gray-500">
                  Viser {snapshots.length} av {totalCount}
                </p>
              </div>
            </div>
          </div>

          {/* Right Panel - Comparison View */}
          <div className="flex-1 overflow-y-auto">
            {selectedSnapshot ? (
              <div className="p-6">
                <h2 className="mb-4 text-lg font-bold text-gray-900">
                  Sammenligning: {selectedSnapshot.label}
                </h2>

                {/* Tabs */}
                <div className="mb-6 flex gap-2">
                  <button
                    onClick={() => setActiveTab('overview')}
                    className={`rounded px-4 py-2 text-sm font-semibold ${
                      activeTab === 'overview'
                        ? 'text-white'
                        : 'border text-gray-700'
                    }`}
                    style={{
                      backgroundColor: activeTab === 'overview' ? colors.button.primary.bg : 'transparent',
                      borderColor: colors.border.medium,
                    }}
                  >
                    📊 Oversikt
                  </button>
                  <button
                    onClick={() => setActiveTab('gantt')}
                    className={`rounded px-4 py-2 text-sm font-semibold ${
                      activeTab === 'gantt'
                        ? 'text-white'
                        : 'border text-gray-700'
                    }`}
                    style={{
                      backgroundColor: activeTab === 'gantt' ? colors.button.primary.bg : 'transparent',
                      borderColor: colors.border.medium,
                    }}
                  >
                    📈 Gantt
                  </button>
                  <button
                    onClick={() => setActiveTab('precedence')}
                    className={`rounded px-4 py-2 text-sm font-semibold ${
                      activeTab === 'precedence'
                        ? 'text-white'
                        : 'border text-gray-700'
                    }`}
                    style={{
                      backgroundColor: activeTab === 'precedence' ? colors.button.primary.bg : 'transparent',
                      borderColor: colors.border.medium,
                    }}
                  >
                    🔀 Presedensdiagram
                  </button>
                </div>

                {/* Overview Tab */}
                {activeTab === 'overview' && (
                  <div className="space-y-6">
                    {/* Budget Summary */}
                    <div
                      className="rounded-lg border p-6"
                      style={{
                        backgroundColor: colors.background.input,
                        borderColor: colors.border.light,
                      }}
                    >
                      <h3 className="mb-4 text-sm font-bold text-gray-900">BUDSJETT OVERSIKT</h3>
                      <div className="space-y-3">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-700">Kontraktfestet:</span>
                          <span className="text-sm font-semibold text-gray-900">
                            {formatBudget(selectedSnapshot.budget_committed)} MNOK
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-700">Tilgjengelig:</span>
                          <span className="text-sm font-semibold text-green-700">
                            {formatBudget(selectedSnapshot.budget_available)} MNOK
                          </span>
                        </div>
                        <div className="flex justify-between border-t pt-3" style={{ borderColor: colors.border.light }}>
                          <span className="text-sm font-semibold text-gray-900">Total budsjett:</span>
                          <span className="text-sm font-semibold text-gray-900">
                            {formatBudget(selectedSnapshot.budget_total)} MNOK
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Timeline */}
                    <div
                      className="rounded-lg border p-6"
                      style={{
                        backgroundColor: colors.background.input,
                        borderColor: colors.border.light,
                      }}
                    >
                      <h3 className="mb-4 text-sm font-bold text-gray-900">TIDSLINJE</h3>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-700">Prosjektslutt (estimert):</span>
                          <span className="text-sm font-semibold text-gray-900">
                            {formatDate(selectedSnapshot.project_end_date)}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-700">Dager før fristen:</span>
                          <span
                            className={`text-sm font-semibold ${
                              selectedSnapshot.days_before_deadline > 0 ? 'text-green-700' : 'text-red-700'
                            }`}
                          >
                            {selectedSnapshot.days_before_deadline > 0 ? '+' : ''}
                            {selectedSnapshot.days_before_deadline} dager
                          </span>
                        </div>
                      </div>
                    </div>

                    {/* Export Button */}
                    <button
                      onClick={exportHistory}
                      className="w-full rounded border px-4 py-3 text-sm font-semibold transition-colors"
                      style={{
                        borderColor: colors.border.medium,
                        backgroundColor: colors.background.card,
                      }}
                    >
                      📥 Eksporter fullstendig historikk (JSON)
                    </button>
                  </div>
                )}

                {/* Gantt Tab */}
                {activeTab === 'gantt' && (
                  <div>
                    <GanttChart
                      wbsItems={wbsItems}
                      commitments={[]}
                      timeline={selectedSnapshot.gantt_state}
                    />
                  </div>
                )}

                {/* Precedence Tab */}
                {activeTab === 'precedence' && (
                  <div>
                    <PrecedenceDiagram
                      wbsItems={wbsItems}
                      timeline={selectedSnapshot.precedence_state}
                    />
                  </div>
                )}
              </div>
            ) : (
              <div className="flex h-full items-center justify-center">
                <p className="text-sm text-gray-500">Velg et snapshot fra tidslinjen</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

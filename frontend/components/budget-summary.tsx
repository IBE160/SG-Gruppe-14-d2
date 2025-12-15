"use client";

import { colors, getBudgetProgressColor } from '@/lib/design-system';
import type { GameSession } from '@/types';

interface BudgetSummaryProps {
  session: GameSession;
}

export function BudgetSummary({ session }: BudgetSummaryProps) {
  const tier1Percentage = session.budget_tier1_percentage || 0;
  const progressColor = getBudgetProgressColor(tier1Percentage);

  const formatMNOK = (amount: number) => {
    return `${(amount / 1_000_000).toFixed(0)} MNOK`;
  };

  return (
    <div
      className="rounded-lg border p-4"
      style={{
        backgroundColor: colors.background.card,
        borderColor: colors.border.medium,
      }}
    >
      <h3 className="mb-3 text-sm font-bold text-gray-900">Budsjett</h3>

      {/* Current Usage */}
      <div className="mb-3">
        <div className="mb-1 flex items-center justify-between">
          <span className="text-xs text-gray-600">Brukt</span>
          <span className="text-sm font-semibold text-gray-900">
            {formatMNOK(session.current_budget_used)}
          </span>
        </div>
        <div className="mb-1 flex items-center justify-between">
          <span className="text-xs text-gray-600">Tilgjengelig</span>
          <span className="text-sm font-semibold text-gray-900">
            {formatMNOK(session.available_budget)}
          </span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-600">Gjenstår</span>
          <span className="text-sm font-semibold text-gray-900">
            {formatMNOK(session.budget_remaining || session.available_budget)}
          </span>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="relative h-4 w-full overflow-hidden rounded-full bg-gray-200">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{
            width: `${Math.min(tier1Percentage, 100)}%`,
            backgroundColor: progressColor,
          }}
        />
      </div>
      <p className="mt-1 text-center text-xs text-gray-600">{tier1Percentage.toFixed(0)}% brukt</p>

      {/* Deadline */}
      <div className="mt-4 border-t pt-3" style={{ borderColor: colors.border.light }}>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-600">Frist</span>
          <span className="text-sm font-semibold text-gray-900">
            {new Date(session.deadline_date).toLocaleDateString('nb-NO', {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
            })}
          </span>
        </div>
        {session.projected_completion_date && (
          <div className="mt-1 flex items-center justify-between">
            <span className="text-xs text-gray-600">Estimert ferdig</span>
            <span
              className="text-sm font-semibold"
              style={{
                color: session.is_timeline_valid
                  ? colors.status.success.text
                  : colors.status.error.text,
              }}
            >
              {new Date(session.projected_completion_date).toLocaleDateString('nb-NO', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
              })}
            </span>
          </div>
        )}
      </div>

      {/* Status */}
      <div className="mt-4 border-t pt-3" style={{ borderColor: colors.border.light }}>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-600">Status</span>
          <span
            className="rounded-full px-2 py-1 text-xs font-semibold"
            style={{
              backgroundColor:
                session.status === 'completed'
                  ? colors.status.success.bg
                  : session.status === 'in_progress'
                    ? colors.budget.tier1.bg
                    : colors.status.error.bg,
              color:
                session.status === 'completed'
                  ? colors.status.success.text
                  : session.status === 'in_progress'
                    ? colors.budget.tier1.text
                    : colors.status.error.text,
            }}
          >
            {session.status === 'completed'
              ? 'Fullført'
              : session.status === 'in_progress'
                ? 'Pågår'
                : 'Avbrutt'}
          </span>
        </div>
      </div>

      {/* Total Budget (Locked + Available) */}
      <div className="mt-4 border-t pt-3" style={{ borderColor: colors.border.light }}>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-600">Totalt budsjett</span>
          <span className="text-sm font-bold text-gray-900">
            {formatMNOK(session.total_budget)}
          </span>
        </div>
        <p className="mt-1 text-xs text-gray-500">
          Låst: {formatMNOK(session.locked_budget)} | Forhandlbar:{' '}
          {formatMNOK(session.available_budget)}
        </p>
      </div>
    </div>
  );
}

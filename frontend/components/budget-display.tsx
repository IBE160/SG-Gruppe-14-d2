"use client";

import { colors, getBudgetProgressColor } from '@/lib/design-system';
import type { GameSession } from '@/types';

interface BudgetDisplayProps {
  session: GameSession;
  showDetails?: boolean;
}

export function BudgetDisplay({ session, showDetails = true }: BudgetDisplayProps) {
  // Calculate percentages
  const tier1Percentage = session.budget_tier1_percentage || 0;
  const tier3Percentage =
    ((session.locked_budget + session.current_budget_used) / session.total_budget) * 100;

  // Get progress bar color
  const progressColor = getBudgetProgressColor(tier1Percentage);

  // Format amounts
  const formatMNOK = (amount: number) => {
    return `${(amount / 1_000_000).toFixed(0)} MNOK`;
  };

  return (
    <div className="space-y-4">
      {/* Section Title */}
      {showDetails && (
        <div className="mb-4">
          <h2 className="text-base font-bold text-gray-900">Prosjektbudsjett</h2>
          <p className="text-xs text-gray-600">
            3 forhandlbare pakker | 12 låste pakker ({formatMNOK(session.locked_budget)})
          </p>
        </div>
      )}

      {/* TIER 1: Tilgjengelig (Available) */}
      <div
        className="rounded-md border p-4"
        style={{
          backgroundColor: colors.budget.tier1.bg,
          borderColor: colors.border.medium,
        }}
      >
        <div className="mb-3 flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">
            Tilgjengelig budsjett (3 forhandlbare pakker)
          </span>
          <span className="text-lg font-bold text-gray-900">
            {formatMNOK(session.current_budget_used)} / {formatMNOK(session.available_budget)}
          </span>
        </div>

        {/* Progress bar */}
        <div className="relative h-5 w-full overflow-hidden rounded-full bg-gray-200">
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{
              width: `${Math.min(tier1Percentage, 100)}%`,
              backgroundColor: progressColor,
            }}
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xs text-gray-700">
              {tier1Percentage.toFixed(0)}% brukt -{' '}
              {formatMNOK(session.budget_remaining || session.available_budget)} gjenstår
            </span>
          </div>
        </div>
      </div>

      {/* TIER 2: Låst (Locked) */}
      <div
        className="rounded-md border p-4"
        style={{
          backgroundColor: colors.budget.tier2.bg,
          borderColor: colors.border.medium,
        }}
      >
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">
            Låst budsjett (12 kontraktfestede pakker)
          </span>
          <span className="text-sm text-gray-700">{formatMNOK(session.locked_budget)}</span>
        </div>
        <p className="mt-1 text-xs text-gray-600">
          Dette budsjettet er allerede forpliktet og kan ikke endres
        </p>
      </div>

      {/* TIER 3: Totalt (Total) */}
      <div
        className="rounded-md border p-4"
        style={{
          backgroundColor: colors.budget.tier3.bg,
          borderColor: colors.border.medium,
        }}
      >
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">Totalt budsjett</span>
          <div className="text-right">
            <span className="text-lg font-bold text-gray-900">
              {formatMNOK(session.locked_budget + session.current_budget_used)} /{' '}
              {formatMNOK(session.total_budget)}
            </span>
            <p className="text-xs text-gray-600">
              {tier3Percentage.toFixed(0)}% brukt |{' '}
              {formatMNOK(
                session.total_budget - session.locked_budget - session.current_budget_used
              )}{' '}
              gjenstår ✓
            </p>
          </div>
        </div>
      </div>

      {/* Warning Banner (if over budget or close to limit) */}
      {tier1Percentage > 0 && (
        <div
          className="rounded-md border-2 p-4"
          style={{
            backgroundColor:
              tier1Percentage >= 100
                ? colors.status.error.bg
                : tier1Percentage >= 90
                  ? colors.status.warning.bg
                  : colors.status.success.bg,
            borderColor:
              tier1Percentage >= 100
                ? colors.status.error.border
                : tier1Percentage >= 90
                  ? colors.status.warning.border
                  : colors.status.success.border,
          }}
        >
          {tier1Percentage >= 100 ? (
            <>
              <p className="text-sm font-bold text-red-900">⚠ BUDSJETTOVERSKRIDELSE</p>
              <p className="mt-1 text-xs text-red-800">
                Du har overskredet det tilgjengelige budsjettet. Du må forhandle ned kostnader
                eller avslå noen forpliktelser.
              </p>
            </>
          ) : tier1Percentage >= 90 ? (
            <>
              <p className="text-sm font-bold text-orange-900">⚠ BUDSJETTADVARSEL</p>
              <p className="mt-1 text-xs text-orange-800">
                Du nærmer deg budsjettgrensen. Kun {formatMNOK(session.budget_remaining || 0)}{' '}
                gjenstår.
              </p>
            </>
          ) : (
            <>
              <p className="text-sm font-bold text-green-900">✓ GODT INNENFOR BUDSJETT</p>
              <p className="mt-1 text-xs text-green-800">
                Du har brukt {formatMNOK(session.current_budget_used)} av tilgjengelig budsjett.
                Fortsett å forhandle for å holde deg under {formatMNOK(session.available_budget)}.
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

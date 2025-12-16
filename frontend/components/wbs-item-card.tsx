"use client";

import { colors } from '@/lib/design-system';
import type { WBSItem } from '@/types';
import { getAgentName } from '@/lib/api/agent-status';

interface WBSItemCardProps {
  item: WBSItem;
  onContact?: (agentId: string) => void;
  isLocked?: boolean;
}

export function WBSItemCard({ item, onContact, isLocked = false }: WBSItemCardProps) {
  const formatMNOK = (amount: number) => {
    return `${(amount / 1_000_000).toFixed(0)} MNOK`;
  };

  const formatDuration = (months: number) => {
    return `${months.toString().replace('.', ',')} mnd`;
  };

  // Status indicator
  const getStatusInfo = () => {
    switch (item.status) {
      case 'committed':
        return {
          emoji: '✓',
          label: 'Godtatt',
          color: colors.status.success.border,
        };
      case 'in_progress':
        return {
          emoji: '💬',
          label: 'Under forhandling',
          color: colors.button.primary.bg,
        };
      case 'rejected':
        return {
          emoji: '✗',
          label: 'Avslått',
          color: colors.status.error.border,
        };
      default:
        return {
          emoji: '⚪',
          label: 'Venter',
          color: colors.text.quaternary,
        };
    }
  };

  const statusInfo = getStatusInfo();

  return (
    <div
      className={`group relative rounded-lg border-2 p-6 transition-all ${
        isLocked ? 'cursor-not-allowed opacity-70' : 'hover:shadow-md'
      }`}
      style={{
        backgroundColor: item.is_negotiable ? colors.wbs.negotiable.bg : colors.wbs.locked.bg,
        borderColor: item.is_negotiable ? colors.wbs.negotiable.border : colors.wbs.locked.border,
      }}
    >
      {/* Left accent bar */}
      <div
        className="absolute left-0 top-0 h-full w-1 rounded-l-lg"
        style={{
          backgroundColor: item.is_negotiable
            ? colors.wbs.negotiable.leftBar
            : colors.wbs.locked.leftBar,
        }}
      />

      {/* Status dot */}
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div
            className="h-2 w-2 rounded-full"
            style={{
              backgroundColor: item.is_negotiable ? colors.wbs.negotiable.dot : colors.border.dark,
            }}
          />
          <h3 className="text-sm font-bold text-gray-900">{item.name}</h3>

          {/* Badge */}
          {item.is_negotiable ? (
            <span
              className="rounded-full px-3 py-1 text-xs font-semibold"
              style={{
                backgroundColor: colors.badge.negotiable.bg,
                borderColor: colors.badge.negotiable.border,
                color: colors.badge.negotiable.text,
                border: '1px solid',
              }}
            >
              💬 Kan forhandles
            </span>
          ) : (
            <span
              className="rounded-full px-3 py-1 text-xs font-semibold"
              style={{
                backgroundColor: colors.badge.locked.bg,
                borderColor: colors.badge.locked.border,
                color: colors.badge.locked.text,
                border: '1px solid',
              }}
            >
              Kontraktfestet
            </span>
          )}
        </div>

        {/* Status */}
        <div className="flex items-center gap-2">
          <span className="text-sm" style={{ color: statusInfo.color }}>
            {statusInfo.emoji} {statusInfo.label}
          </span>
        </div>
      </div>

      {/* Details */}
      <div className="space-y-1">
        <p className="text-xs text-gray-600">
          Leverandør: {getAgentName(item.agent_id)} | Varighet: {formatDuration(item.baseline_duration)}
        </p>

        {item.is_negotiable ? (
          <>
            <p className="text-xs text-gray-600">Baseline: {formatMNOK(item.baseline_cost)}</p>
            {item.committed_cost && (
              <p className="text-xs font-semibold text-green-700">
                Godtatt: {formatMNOK(item.committed_cost)} (spart{' '}
                {formatMNOK(item.baseline_cost - item.committed_cost)})
              </p>
            )}
          </>
        ) : (
          <p className="text-xs text-gray-500">Kostnad: {formatMNOK(item.baseline_cost)}</p>
        )}

        {item.is_critical_path && (
          <p className="text-xs font-semibold text-orange-600">⚠ Kritisk sti</p>
        )}
      </div>

      {/* Contact button (only for negotiable items) */}
      {item.is_negotiable && onContact && !isLocked && item.status !== 'committed' && (
        <button
          onClick={() => onContact(item.agent_id)}
          className="mt-4 rounded px-6 py-2 text-xs font-semibold text-white transition-colors"
          style={{
            backgroundColor: colors.button.primary.bg,
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.backgroundColor = colors.button.primary.hover;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.backgroundColor = colors.button.primary.bg;
          }}
        >
          Kontakt
        </button>
      )}
    </div>
  );
}

// Locked items preview component
export function LockedItemsPreview({ count = 12, totalCost }: { count: number; totalCost: number }) {
  const formatMNOK = (amount: number) => {
    return `${(amount / 1_000_000).toFixed(0)} MNOK`;
  };

  return (
    <div
      className="rounded-lg border p-6 opacity-70"
      style={{
        backgroundColor: colors.wbs.locked.bg,
        borderColor: colors.wbs.locked.border,
      }}
    >
      {/* Left accent bar */}
      <div
        className="absolute left-0 top-0 h-full w-0.5 rounded-l-lg"
        style={{
          backgroundColor: colors.wbs.locked.leftBar,
        }}
      />

      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-gray-600">
          🔒 {count} låste pakker (kontraktfestet)
        </span>
        <span
          className="rounded-full px-3 py-1 text-xs font-semibold"
          style={{
            backgroundColor: colors.badge.locked.bg,
            borderColor: colors.badge.locked.border,
            color: colors.badge.locked.text,
            border: '1px solid',
          }}
        >
          Kontraktfestet
        </span>
      </div>

      <p className="mt-2 text-xs text-gray-600">
        Eksempler: Prosjektering (30 MNOK), RIB (25 MNOK), Elektrisk (35 MNOK)...
      </p>
      <p className="mt-1 text-xs text-gray-500">
        Totalt {formatMNOK(totalCost)} fordelt på {count} pakker som allerede er forhandlet
      </p>
    </div>
  );
}

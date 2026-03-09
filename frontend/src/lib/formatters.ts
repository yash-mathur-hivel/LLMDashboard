import { format, formatDistanceToNow } from "date-fns";

export function formatDate(dateStr: string): string {
  if (!dateStr) return "—";
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return "—";
  return format(date, "MMM d, yyyy HH:mm:ss");
}

export function formatRelative(dateStr: string): string {
  if (!dateStr) return "—";
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return "—";
  return formatDistanceToNow(date, { addSuffix: true });
}

export function formatCost(cost: number | null): string {
  if (cost === null || cost === undefined) return "—";
  if (cost === 0) return "$0.00";
  if (cost < 0.0001) return `$${cost.toExponential(2)}`;
  return `$${cost.toFixed(6)}`;
}

export function formatTokens(n: number | null): string {
  if (n === null || n === undefined) return "—";
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return n.toLocaleString();
}

export function formatLatency(ms: number | null): string {
  if (ms === null || ms === undefined) return "—";
  if (ms >= 1000) return `${(ms / 1000).toFixed(1)}s`;
  return `${ms}ms`;
}

export function formatNumber(n: number | null): string {
  if (n === null || n === undefined || Number.isNaN(n)) return "—";
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return n.toLocaleString();
}

export const PROVIDER_COLORS: Record<string, string> = {
  openai: "#10b981",
  anthropic: "#f59e0b",
  gemini: "#3b82f6",
  openai_compatible: "#8b5cf6",
};

export const CHART_COLORS = [
  "#2563eb",
  "#10b981",
  "#f59e0b",
  "#ef4444",
  "#8b5cf6",
  "#06b6d4",
  "#f97316",
];

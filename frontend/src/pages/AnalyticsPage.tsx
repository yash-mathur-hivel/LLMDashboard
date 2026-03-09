import { useState } from "react";
import { Topbar } from "@/components/layout/Topbar";
import { MetricCard } from "@/components/analytics/MetricCard";
import { TimeSeriesChart } from "@/components/analytics/TimeSeriesChart";
import { BreakdownBarChart } from "@/components/analytics/BreakdownBarChart";
import { useAnalyticsSummary, useTimeseries } from "@/hooks/useAnalytics";
import { formatCost, formatNumber, formatLatency, formatTokens } from "@/lib/formatters";
import type { AnalyticsFilters } from "@/types/analytics";
import { BarChart2, DollarSign, Hash, Clock, AlertCircle } from "lucide-react";

const GROUP_BY_OPTIONS = ["model", "provider", "masked_api_key", "origin_domain", "label"];
const GRANULARITY_OPTIONS = ["hour", "day", "week"] as const;

export function AnalyticsPage() {
  const [filters, setFilters] = useState<AnalyticsFilters>({
    granularity: "day",
    group_by: "model",
  });

  const { data: summary, isLoading } = useAnalyticsSummary(filters);
  const { data: timeseries } = useTimeseries(filters);

  const set = <K extends keyof AnalyticsFilters>(k: K, v: AnalyticsFilters[K]) =>
    setFilters((f) => ({ ...f, [k]: v }));

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <Topbar
        title="Analytics"
        actions={
          <div className="flex items-center gap-2">
            <input
              type="date"
              value={filters.start_date ?? ""}
              onChange={(e) => set("start_date", e.target.value || undefined)}
              className="input text-xs"
            />
            <span className="text-[#475569] text-xs">to</span>
            <input
              type="date"
              value={filters.end_date ?? ""}
              onChange={(e) => set("end_date", e.target.value || undefined)}
              className="input text-xs"
            />
            <select
              value={filters.granularity}
              onChange={(e) => set("granularity", e.target.value as AnalyticsFilters["granularity"])}
              className="input text-xs"
            >
              {GRANULARITY_OPTIONS.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
            <select
              value={filters.group_by ?? ""}
              onChange={(e) => set("group_by", e.target.value || undefined)}
              className="input text-xs"
            >
              <option value="">No grouping</option>
              {GROUP_BY_OPTIONS.map((g) => (
                <option key={g} value={g}>
                  by {g}
                </option>
              ))}
            </select>
          </div>
        }
      />

      <div className="flex-1 overflow-y-auto px-6 py-5 space-y-6">
        {isLoading && (
          <p className="text-[#475569] text-sm">Loading…</p>
        )}

        {summary && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <MetricCard
                label="Total Requests"
                value={formatNumber(summary.total_requests)}
                sub={`${summary.error_count} errors`}
                icon={<BarChart2 size={20} />}
              />
              <MetricCard
                label="Total Cost"
                value={formatCost(summary.total_cost_usd)}
                icon={<DollarSign size={20} />}
              />
              <MetricCard
                label="Total Tokens"
                value={formatTokens(
                  summary.total_prompt_tokens + summary.total_completion_tokens
                )}
                sub={`${formatTokens(summary.total_prompt_tokens)} in / ${formatTokens(summary.total_completion_tokens)} out`}
                icon={<Hash size={20} />}
              />
              <MetricCard
                label="Avg Latency"
                value={formatLatency(summary.avg_latency_ms)}
                sub={`p95: ${formatLatency(summary.p95_latency_ms)}`}
                icon={<Clock size={20} />}
              />
            </div>

            {timeseries && timeseries.data.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <TimeSeriesChart
                  data={timeseries.data}
                  metric="total_requests"
                  label="Requests over time"
                  color="#2563eb"
                />
                <TimeSeriesChart
                  data={timeseries.data}
                  metric="total_cost_usd"
                  label="Cost over time"
                  color="#10b981"
                />
                <TimeSeriesChart
                  data={timeseries.data}
                  metric="avg_latency_ms"
                  label="Avg latency over time"
                  color="#f59e0b"
                />
              </div>
            )}

            {summary.breakdown.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <BreakdownBarChart
                  data={summary.breakdown}
                  metric="total_requests"
                  label={`Requests by ${filters.group_by ?? "dimension"}`}
                />
                <BreakdownBarChart
                  data={summary.breakdown}
                  metric="total_cost_usd"
                  label={`Cost by ${filters.group_by ?? "dimension"}`}
                />
              </div>
            )}

            {summary.total_requests === 0 && (
              <div className="flex flex-col items-center justify-center py-20 text-[#475569]">
                <AlertCircle size={40} className="mb-3 opacity-30" />
                <p className="text-sm">No data yet. Send some requests through the proxy!</p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

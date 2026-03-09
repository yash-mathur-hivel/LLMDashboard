import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";
import { format } from "date-fns";
import type { TimeseriesPoint } from "@/types/analytics";

interface TimeSeriesChartProps {
  data: TimeseriesPoint[];
  metric: "total_requests" | "total_cost_usd" | "avg_latency_ms";
  label: string;
  color?: string;
}

function formatBucket(bucket: string) {
  try {
    return format(new Date(bucket), "MMM d");
  } catch {
    return bucket;
  }
}

function formatValue(metric: string, value: number | null): string {
  if (value === null) return "—";
  if (metric === "total_cost_usd") return `$${value.toFixed(4)}`;
  if (metric === "avg_latency_ms") return `${Math.round(value)}ms`;
  return value.toLocaleString();
}

export function TimeSeriesChart({ data, metric, label, color = "#2563eb" }: TimeSeriesChartProps) {
  const chartData = data.map((d) => ({
    bucket: formatBucket(d.bucket),
    value: d[metric] ?? 0,
  }));

  return (
    <div className="bg-[#0a0a0a] border border-[#1e293b] rounded-lg p-5">
      <p className="text-sm font-medium text-[#94a3b8] mb-4">{label}</p>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="bucket"
            tick={{ fill: "#475569", fontSize: 11 }}
            axisLine={{ stroke: "#1e293b" }}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "#475569", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            width={50}
          />
          <Tooltip
            contentStyle={{
              background: "#111111",
              border: "1px solid #1e293b",
              borderRadius: 6,
              color: "#f1f5f9",
              fontSize: 12,
            }}
            formatter={(value) => [formatValue(metric, value as number | null), label]}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke={color}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: color }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

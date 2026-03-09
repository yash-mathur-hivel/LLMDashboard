import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from "recharts";
import type { BreakdownItem } from "@/types/analytics";
import { CHART_COLORS } from "@/lib/formatters";

interface BreakdownBarChartProps {
  data: BreakdownItem[];
  metric: "total_requests" | "total_cost_usd" | "avg_latency_ms";
  label: string;
}

function WrappedTick({ x, y, payload }: { x?: number; y?: number; payload?: { value: string } }) {
  const words = (payload?.value ?? "").split("-");
  // Split into two lines: first half and second half of dash-separated parts
  const mid = Math.ceil(words.length / 2);
  const line1 = words.slice(0, mid).join("-");
  const line2 = words.slice(mid).join("-");
  return (
    <g transform={`translate(${x},${y})`}>
      <text x={0} y={-6} textAnchor="end" fill="#94a3b8" fontSize={11}>
        {line1}
      </text>
      {line2 && (
        <text x={0} y={8} textAnchor="end" fill="#94a3b8" fontSize={11}>
          {line2}
        </text>
      )}
    </g>
  );
}

export function BreakdownBarChart({ data, metric, label }: BreakdownBarChartProps) {
  const chartData = data.slice(0, 10).map((d) => ({
    name: d.dimension ?? "(none)",
    value: d[metric] ?? 0,
  }));

  return (
    <div className="bg-[#0a0a0a] border border-[#1e293b] rounded-lg p-5">
      <p className="text-sm font-medium text-[#94a3b8] mb-4">{label}</p>
      <ResponsiveContainer width="100%" height={Math.max(220, chartData.length * 52)}>
        <BarChart
          data={chartData}
          layout="vertical"
          margin={{ top: 0, right: 16, left: 0, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
          <XAxis
            type="number"
            tick={{ fill: "#475569", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            type="category"
            dataKey="name"
            tick={<WrappedTick />}
            axisLine={false}
            tickLine={false}
            width={140}
          />
          <Tooltip
            contentStyle={{
              background: "#111111",
              border: "1px solid #1e293b",
              borderRadius: 6,
              color: "#f1f5f9",
              fontSize: 12,
            }}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {chartData.map((_, i) => (
              <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

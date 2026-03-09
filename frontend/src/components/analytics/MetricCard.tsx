import React from "react";

interface MetricCardProps {
  label: string;
  value: string;
  sub?: string;
  icon?: React.ReactNode;
}

export function MetricCard({ label, value, sub, icon }: MetricCardProps) {
  return (
    <div className="bg-[#0a0a0a] border border-[#1e293b] rounded-lg p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-[#94a3b8] uppercase tracking-wider mb-1">{label}</p>
          <p className="text-2xl font-semibold text-white">{value}</p>
          {sub && <p className="text-xs text-[#475569] mt-1">{sub}</p>}
        </div>
        {icon && <div className="text-[#2563eb]">{icon}</div>}
      </div>
    </div>
  );
}

import type { ReactNode } from "react";

interface TopbarProps {
  title: string;
  actions?: ReactNode;
}

export function Topbar({ title, actions }: TopbarProps) {
  return (
    <div className="h-14 border-b border-[#1e293b] bg-[#000000] flex items-center justify-between px-6 shrink-0">
      <h1 className="text-base font-semibold text-white">{title}</h1>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}

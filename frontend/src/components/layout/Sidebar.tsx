import { NavLink } from "react-router-dom";
import { BarChart2, List, Server, Activity } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV = [
  { to: "/", label: "Analytics", icon: BarChart2 },
  { to: "/logs", label: "Logs", icon: List },
  { to: "/mcp", label: "MCP Servers", icon: Server },
];

export function Sidebar() {
  return (
    <aside className="w-56 shrink-0 border-r border-[#1e293b] bg-[#0a0a0a] flex flex-col">
      <div className="h-14 flex items-center px-4 border-b border-[#1e293b]">
        <Activity className="text-[#2563eb] mr-2" size={20} />
        <span className="font-semibold text-sm text-white tracking-wide">LLM Dashboard</span>
      </div>
      <nav className="flex-1 py-4 px-2 space-y-1">
        {NAV.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === "/"}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors",
                isActive
                  ? "bg-[#1e3a8a] text-white"
                  : "text-[#94a3b8] hover:text-white hover:bg-[#111111]"
              )
            }
          >
            <Icon size={16} />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

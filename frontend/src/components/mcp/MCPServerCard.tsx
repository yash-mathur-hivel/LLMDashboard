import { Pencil, Trash2 } from "lucide-react";
import type { MCPServer } from "@/types/mcp";
import { formatDate } from "@/lib/formatters";
import { cn } from "@/lib/utils";

interface MCPServerCardProps {
  server: MCPServer;
  onEdit: (server: MCPServer) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

export function MCPServerCard({ server, onEdit, onDelete, onToggle }: MCPServerCardProps) {
  return (
    <div className="bg-[#0a0a0a] border border-[#1e293b] rounded-lg p-5">
      <div className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold text-white">{server.name}</h3>
            <span className="text-xs px-2 py-0.5 rounded-full bg-[#1e293b] text-[#94a3b8]">
              {server.transport}
            </span>
          </div>
          <div className="mt-2 space-y-1">
            {server.command && (
              <p className="text-xs font-mono text-[#64748b]">
                {server.command} {server.args?.join(" ")}
              </p>
            )}
            {server.url && (
              <p className="text-xs font-mono text-[#64748b]">{server.url}</p>
            )}
            <p className="text-xs text-[#475569]">Added {formatDate(server.created_at)}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => onToggle(server.id)}
            className={cn(
              "relative inline-flex h-5 w-9 rounded-full transition-colors",
              server.enabled ? "bg-[#2563eb]" : "bg-[#1e293b]"
            )}
          >
            <span
              className={cn(
                "inline-block h-4 w-4 rounded-full bg-white transition-transform mt-0.5",
                server.enabled ? "translate-x-4" : "translate-x-0.5"
              )}
            />
          </button>
          <button
            onClick={() => onEdit(server)}
            className="text-[#475569] hover:text-white transition-colors"
          >
            <Pencil size={14} />
          </button>
          <button
            onClick={() => onDelete(server.id)}
            className="text-[#475569] hover:text-red-400 transition-colors"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}

import { useState } from "react";
import { Topbar } from "@/components/layout/Topbar";
import { MCPServerCard } from "@/components/mcp/MCPServerCard";
import { MCPServerForm } from "@/components/mcp/MCPServerForm";
import { useMCPServers, useCreateMCPServer, useUpdateMCPServer, useDeleteMCPServer, useToggleMCPServer } from "@/hooks/useMCP";
import type { MCPServer, MCPServerCreate } from "@/types/mcp";
import { Plus, Server } from "lucide-react";

export function MCPPage() {
  const { data: servers, isLoading } = useMCPServers();
  const create = useCreateMCPServer();
  const update = useUpdateMCPServer();
  const del = useDeleteMCPServer();
  const toggle = useToggleMCPServer();

  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<MCPServer | null>(null);

  const handleSubmit = (data: MCPServerCreate) => {
    if (editing) {
      update.mutate(
        { id: editing.id, body: data },
        { onSuccess: () => { setEditing(null); setShowForm(false); } }
      );
    } else {
      create.mutate(data, { onSuccess: () => setShowForm(false) });
    }
  };

  const handleEdit = (server: MCPServer) => {
    setEditing(server);
    setShowForm(true);
  };

  const handleDelete = (id: string) => {
    if (confirm("Delete this MCP server?")) {
      del.mutate(id);
    }
  };

  return (
    <div className="flex flex-col h-full overflow-hidden">
      <Topbar
        title="MCP Servers"
        actions={
          <button
            onClick={() => { setEditing(null); setShowForm(true); }}
            className="flex items-center gap-1.5 text-sm px-3 py-1.5 bg-[#2563eb] text-white rounded-md hover:bg-[#1d4ed8] transition-colors"
          >
            <Plus size={14} />
            Add Server
          </button>
        }
      />

      <div className="flex-1 overflow-y-auto px-6 py-5">
        {isLoading && (
          <p className="text-[#475569] text-sm">Loading…</p>
        )}

        {servers && servers.length === 0 && (
          <div className="flex flex-col items-center justify-center py-20 text-[#475569]">
            <Server size={40} className="mb-3 opacity-30" />
            <p className="text-sm mb-4">No MCP servers configured</p>
            <button
              onClick={() => { setEditing(null); setShowForm(true); }}
              className="text-sm px-4 py-2 bg-[#2563eb] text-white rounded-md hover:bg-[#1d4ed8] transition-colors"
            >
              Add your first server
            </button>
          </div>
        )}

        {servers && servers.length > 0 && (
          <div className="grid gap-4 max-w-3xl">
            {servers.map((server) => (
              <MCPServerCard
                key={server.id}
                server={server}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onToggle={(id) => toggle.mutate(id)}
              />
            ))}
          </div>
        )}
      </div>

      {showForm && (
        <MCPServerForm
          initial={editing}
          onSubmit={handleSubmit}
          onClose={() => { setShowForm(false); setEditing(null); }}
          isLoading={create.isPending || update.isPending}
        />
      )}
    </div>
  );
}

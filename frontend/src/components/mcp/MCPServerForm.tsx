import { useState } from "react";
import type { MCPServer, MCPServerCreate } from "@/types/mcp";
import { X } from "lucide-react";

interface MCPServerFormProps {
  initial?: MCPServer | null;
  onSubmit: (data: MCPServerCreate) => void;
  onClose: () => void;
  isLoading?: boolean;
}

const EMPTY: MCPServerCreate = {
  name: "",
  transport: "stdio",
  command: null,
  args: null,
  url: null,
  headers: null,
  env_vars: null,
  enabled: true,
};

export function MCPServerForm({ initial, onSubmit, onClose, isLoading }: MCPServerFormProps) {
  const [form, setForm] = useState<MCPServerCreate>(
    initial
      ? {
          name: initial.name,
          transport: initial.transport,
          command: initial.command,
          args: initial.args,
          url: initial.url,
          headers: initial.headers,
          env_vars: initial.env_vars,
          enabled: initial.enabled,
        }
      : { ...EMPTY }
  );
  const [argsStr, setArgsStr] = useState(initial?.args?.join(" ") ?? "");

  const set = <K extends keyof MCPServerCreate>(key: K, value: MCPServerCreate[K]) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({
      ...form,
      args: argsStr.trim() ? argsStr.trim().split(/\s+/) : null,
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="bg-[#0a0a0a] border border-[#1e293b] rounded-xl w-full max-w-lg shadow-2xl">
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#1e293b]">
          <h2 className="text-sm font-semibold text-white">
            {initial ? "Edit MCP Server" : "Add MCP Server"}
          </h2>
          <button onClick={onClose} className="text-[#475569] hover:text-white transition-colors">
            <X size={16} />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="px-6 py-5 space-y-4">
          <Field label="Name">
            <input
              required
              value={form.name}
              onChange={(e) => set("name", e.target.value)}
              className="input w-full"
              placeholder="my-server"
            />
          </Field>

          <Field label="Transport">
            <select
              value={form.transport}
              onChange={(e) => {
                const next = e.target.value as MCPServerCreate["transport"];
                setForm((prev) => ({
                  ...prev,
                  transport: next,
                  command: next === "stdio" ? prev.command : null,
                  args: next === "stdio" ? prev.args : null,
                  url: next === "http" || next === "sse" ? prev.url : null,
                }));
                if (next !== "stdio") {
                  setArgsStr("");
                }
              }}
              className="input w-full"
            >
              <option value="stdio">stdio</option>
              <option value="sse">sse</option>
              <option value="http">http</option>
            </select>
          </Field>

          {form.transport === "stdio" && (
            <>
              <Field label="Command">
                <input
                  value={form.command ?? ""}
                  onChange={(e) => set("command", e.target.value || null)}
                  className="input w-full"
                  placeholder="npx"
                />
              </Field>
              <Field label="Args (space-separated)">
                <input
                  value={argsStr}
                  onChange={(e) => setArgsStr(e.target.value)}
                  className="input w-full"
                  placeholder="-y @modelcontextprotocol/server-filesystem /tmp"
                />
              </Field>
            </>
          )}

          {(form.transport === "sse" || form.transport === "http") && (
            <Field label="URL">
              <input
                value={form.url ?? ""}
                onChange={(e) => set("url", e.target.value || null)}
                className="input w-full"
                placeholder="https://..."
              />
            </Field>
          )}

          <div className="flex items-center gap-2">
            <label
              htmlFor="mcp-enabled"
              className="text-sm text-[#94a3b8]"
            >
              Enabled
            </label>
            <button
              id="mcp-enabled"
              type="button"
              onClick={() => set("enabled", !form.enabled)}
              aria-pressed={form.enabled}
              className={`relative inline-flex h-5 w-9 rounded-full transition-colors ${form.enabled ? "bg-[#2563eb]" : "bg-[#1e293b]"}`}
            >
              <span
                className={`inline-block h-4 w-4 rounded-full bg-white transition-transform mt-0.5 ${form.enabled ? "translate-x-4" : "translate-x-0.5"}`}
              />
            </button>
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm text-[#94a3b8] hover:text-white transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-4 py-2 text-sm font-medium bg-[#2563eb] text-white rounded-md hover:bg-[#1d4ed8] transition-colors disabled:opacity-50"
            >
              {isLoading ? "Saving…" : "Save"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-xs text-[#94a3b8] mb-1">{label}</label>
      {children}
    </div>
  );
}

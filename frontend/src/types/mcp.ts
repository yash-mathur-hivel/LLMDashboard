export interface MCPServer {
  id: string;
  name: string;
  transport: "stdio" | "sse" | "http";
  command: string | null;
  args: string[] | null;
  url: string | null;
  headers: Record<string, string> | null;
  env_vars: Record<string, string> | null;
  enabled: boolean;
  created_at: string;
  updated_at: string;
}

export type MCPServerCreate = Omit<MCPServer, "id" | "created_at" | "updated_at">;
export type MCPServerUpdate = Partial<MCPServerCreate>;

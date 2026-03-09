import client from "./client";
import type { MCPServer, MCPServerCreate, MCPServerUpdate } from "@/types/mcp";

export async function fetchMCPServers(): Promise<MCPServer[]> {
  const { data } = await client.get<MCPServer[]>("/mcp");
  return data;
}

export async function createMCPServer(body: MCPServerCreate): Promise<MCPServer> {
  const { data } = await client.post<MCPServer>("/mcp", body);
  return data;
}

export async function updateMCPServer(id: string, body: MCPServerUpdate): Promise<MCPServer> {
  const { data } = await client.put<MCPServer>(`/mcp/${id}`, body);
  return data;
}

export async function deleteMCPServer(id: string): Promise<void> {
  await client.delete(`/mcp/${id}`);
}

export async function toggleMCPServer(id: string): Promise<MCPServer> {
  const { data } = await client.patch<MCPServer>(`/mcp/${id}/toggle`);
  return data;
}

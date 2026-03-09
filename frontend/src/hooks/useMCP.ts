import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchMCPServers,
  createMCPServer,
  updateMCPServer,
  deleteMCPServer,
  toggleMCPServer,
} from "@/api/mcp";
import type { MCPServerCreate, MCPServerUpdate } from "@/types/mcp";

export function useMCPServers() {
  return useQuery({
    queryKey: ["mcp"],
    queryFn: fetchMCPServers,
    staleTime: 30_000,
  });
}

export function useCreateMCPServer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (body: MCPServerCreate) => createMCPServer(body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mcp"] }),
  });
}

export function useUpdateMCPServer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, body }: { id: string; body: MCPServerUpdate }) =>
      updateMCPServer(id, body),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mcp"] }),
  });
}

export function useDeleteMCPServer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteMCPServer(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mcp"] }),
  });
}

export function useToggleMCPServer() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => toggleMCPServer(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["mcp"] }),
  });
}

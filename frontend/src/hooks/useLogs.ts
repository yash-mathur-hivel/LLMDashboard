import { useQuery } from "@tanstack/react-query";
import { fetchLogs, fetchLog } from "@/api/logs";
import type { LogFilters } from "@/types/log";

export function useLogs(filters: LogFilters = {}) {
  const key = JSON.stringify(filters);
  return useQuery({
    queryKey: ["logs", key],
    queryFn: () => fetchLogs(filters),
    staleTime: 10_000,
  });
}

export function useLogDetail(id: string | null) {
  return useQuery({
    queryKey: ["log", id],
    queryFn: () => fetchLog(id!),
    enabled: !!id,
    staleTime: 30_000,
  });
}

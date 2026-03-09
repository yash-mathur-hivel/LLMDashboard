import { useQuery } from "@tanstack/react-query";
import { fetchLogs, fetchLog } from "@/api/logs";
import type { LogFilters } from "@/types/log";

export function useLogs(filters: LogFilters = {}) {
  return useQuery({
    queryKey: ["logs", filters],
    queryFn: () => fetchLogs(filters),
    staleTime: 10_000,
  });
}

export function useLogDetail(id: string | null) {
  return useQuery({
    queryKey: ["log", id],
    queryFn: () => {
      if (!id) {
        throw new Error("useLogDetail called without an id");
      }
      return fetchLog(id);
    },
    enabled: !!id,
    staleTime: 30_000,
  });
}

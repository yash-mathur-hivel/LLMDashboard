import { useQuery } from "@tanstack/react-query";
import { fetchSummary, fetchTimeseries, fetchDimensions } from "@/api/analytics";
import type { AnalyticsFilters } from "@/types/analytics";

export function useAnalyticsSummary(filters: AnalyticsFilters = {}) {
  return useQuery({
    queryKey: ["analytics", "summary", filters],
    queryFn: () => fetchSummary(filters),
    staleTime: 30_000,
  });
}

export function useTimeseries(filters: AnalyticsFilters = {}) {
  return useQuery({
    queryKey: ["analytics", "timeseries", filters],
    queryFn: () => fetchTimeseries(filters),
    staleTime: 30_000,
  });
}

export function useDimensions() {
  return useQuery({
    queryKey: ["analytics", "dimensions"],
    queryFn: fetchDimensions,
    staleTime: 60_000,
  });
}

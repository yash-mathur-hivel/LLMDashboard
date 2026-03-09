import client from "./client";
import type {
  AnalyticsFilters,
  SummaryResponse,
  TimeseriesResponse,
  DimensionsResponse,
} from "@/types/analytics";

export async function fetchSummary(filters: AnalyticsFilters = {}): Promise<SummaryResponse> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== "")
  );
  const { data } = await client.get<SummaryResponse>("/analytics/summary", { params });
  return data;
}

export async function fetchTimeseries(filters: AnalyticsFilters = {}): Promise<TimeseriesResponse> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== "")
  );
  const { data } = await client.get<TimeseriesResponse>("/analytics/timeseries", { params });
  return data;
}

export async function fetchDimensions(): Promise<DimensionsResponse> {
  const { data } = await client.get<DimensionsResponse>("/analytics/dimensions");
  return data;
}

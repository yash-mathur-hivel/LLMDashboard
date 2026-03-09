export interface SummaryResponse {
  total_requests: number;
  total_prompt_tokens: number;
  total_completion_tokens: number;
  total_cost_usd: number;
  avg_latency_ms: number;
  p50_latency_ms: number;
  p95_latency_ms: number;
  error_count: number;
  breakdown: BreakdownItem[];
}

export interface BreakdownItem {
  dimension: string | null;
  total_requests: number;
  total_prompt_tokens: number | null;
  total_completion_tokens: number | null;
  total_cost_usd: number | null;
  avg_latency_ms: number | null;
}

export interface TimeseriesPoint {
  bucket: string;
  dimension?: string;
  total_requests: number;
  total_cost_usd: number | null;
  total_prompt_tokens: number | null;
  total_completion_tokens: number | null;
  avg_latency_ms: number | null;
}

export interface TimeseriesResponse {
  data: TimeseriesPoint[];
}

export interface DimensionsResponse {
  providers: string[];
  models: string[];
  masked_api_keys: string[];
  origin_domains: string[];
  labels: string[];
}

export interface AnalyticsFilters {
  start_date?: string;
  end_date?: string;
  group_by?: string;
  granularity?: "hour" | "day" | "week";
}

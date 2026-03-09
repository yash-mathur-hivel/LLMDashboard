import client from "./client";
import type { LogFilters, LogsResponse, RequestLogDetail } from "@/types/log";

export async function fetchLogs(filters: LogFilters = {}): Promise<LogsResponse> {
  const params = Object.fromEntries(
    Object.entries(filters).filter(([, v]) => v !== undefined && v !== "")
  );
  const { data } = await client.get<LogsResponse>("/logs", { params });
  return data;
}

export async function fetchLog(id: string): Promise<RequestLogDetail> {
  const { data } = await client.get<RequestLogDetail>(`/logs/${id}`);
  return data;
}

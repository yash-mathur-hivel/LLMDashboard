export interface RequestLogListItem {
  id: string;
  provider: string;
  model: string;
  masked_api_key: string | null;
  label: string | null;
  origin_domain: string | null;
  requested_at: string;
  latency_ms: number | null;
  prompt_tokens: number | null;
  completion_tokens: number | null;
  cost_usd: number | null;
  finish_reason: string | null;
  status: "success" | "error";
  error_message: string | null;
  http_status_code: number | null;
}

export interface RequestLogDetail extends RequestLogListItem {
  system_prompt: string | null;
  messages: Message[];
  tool_definitions: ToolDefinition[] | null;
  assistant_response: string | null;
  tool_calls: ToolCall[] | null;
  mcp_config_id: string | null;
  raw_response_meta: Record<string, unknown> | null;
}

export interface Message {
  role: "system" | "user" | "assistant" | "tool";
  content: string | MessageContentPart[];
}

export interface MessageContentPart {
  type: string;
  text?: string;
  [key: string]: unknown;
}

export interface ToolCall {
  id: string;
  name: string;
  input: Record<string, unknown>;
}

export interface ToolDefinition {
  name: string;
  description?: string;
  input_schema?: Record<string, unknown>;
  parameters?: Record<string, unknown>;
}

export interface LogsResponse {
  items: RequestLogListItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface LogFilters {
  provider?: string;
  model?: string;
  masked_api_key?: string;
  origin_domain?: string;
  label?: string;
  status?: string;
  start_date?: string;
  end_date?: string;
  search?: string;
  page?: number;
  page_size?: number;
}

import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel


class RequestLogListItem(BaseModel):
    id: uuid.UUID
    provider: str
    model: str
    masked_api_key: str | None
    label: str | None
    origin_domain: str | None
    requested_at: datetime
    latency_ms: int | None
    prompt_tokens: int | None
    completion_tokens: int | None
    cost_usd: float | None
    finish_reason: str | None
    status: str
    error_message: str | None
    http_status_code: int | None

    model_config = {"from_attributes": True}


class RequestLogDetail(RequestLogListItem):
    system_prompt: str | None
    messages: list[dict[str, Any]]
    tool_definitions: list[dict[str, Any]] | None
    assistant_response: str | None
    tool_calls: list[dict[str, Any]] | None
    mcp_config_id: uuid.UUID | None
    raw_response_meta: dict[str, Any] | None


class LogsResponse(BaseModel):
    items: list[RequestLogListItem]
    total: int
    page: int
    page_size: int
    total_pages: int

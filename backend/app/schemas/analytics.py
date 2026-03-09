from pydantic import BaseModel
from typing import Any


class BreakdownItem(BaseModel):
    dimension: str | None
    total_requests: int
    total_prompt_tokens: int | None
    total_completion_tokens: int | None
    total_cost_usd: float | None
    avg_latency_ms: float | None


class SummaryResponse(BaseModel):
    total_requests: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_cost_usd: float
    avg_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    error_count: int
    breakdown: list[dict[str, Any]]


class TimeseriesResponse(BaseModel):
    data: list[dict[str, Any]]


class DimensionsResponse(BaseModel):
    providers: list[str]
    models: list[str]
    masked_api_keys: list[str]
    origin_domains: list[str]
    labels: list[str]

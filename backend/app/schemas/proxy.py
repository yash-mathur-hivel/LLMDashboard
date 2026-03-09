import uuid
from typing import Any, Literal
from pydantic import BaseModel

ProviderOverride = Literal["openai", "azure", "anthropic", "gemini"]


class ProxyRequest(BaseModel):
    model: str
    api_key: str
    provider: ProviderOverride | None = None  # skips auto-detection when set
    api_endpoint: str | None = None
    label: str | None = None
    mcp_config_id: uuid.UUID | None = None
    system: str | None = None
    user_message: str                          # current user turn (required)
    messages: list[dict[str, Any]] = []        # prior conversation history (optional)
    tools: list[dict[str, Any]] | None = None
    max_tokens: int | None = None
    temperature: float | None = None


class ProxyResponse(BaseModel):
    log_id: str
    provider: str
    model: str
    content: str | None
    tool_calls: list[dict[str, Any]] | None
    finish_reason: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    latency_ms: int
    status: str
    error_message: str | None

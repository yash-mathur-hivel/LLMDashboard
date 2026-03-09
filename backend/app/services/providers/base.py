from dataclasses import dataclass, field
from typing import Any


@dataclass
class NormalizedRequest:
    model: str
    messages: list[dict]  # [{role, content}] OpenAI-style
    system: str | None = None
    tools: list[dict] | None = None  # Anthropic input_schema format
    max_tokens: int | None = None
    temperature: float | None = None


@dataclass
class ToolCall:
    id: str
    name: str
    input: dict


@dataclass
class NormalizedResponse:
    content: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0
    finish_reason: str = "stop"
    raw_meta: dict = field(default_factory=dict)


class BaseProvider:
    def build_request_payload(self, req: NormalizedRequest) -> dict:
        raise NotImplementedError

    def parse_response(self, data: dict) -> NormalizedResponse:
        raise NotImplementedError

    def get_api_url(self, model: str) -> str:
        raise NotImplementedError

    def get_headers(self, api_key: str) -> dict:
        raise NotImplementedError

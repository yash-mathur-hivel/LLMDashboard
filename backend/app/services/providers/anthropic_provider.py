from app.services.providers.base import BaseProvider, NormalizedRequest, NormalizedResponse, ToolCall


class AnthropicProvider(BaseProvider):
    def get_api_url(self, model: str) -> str:
        return "https://api.anthropic.com/v1/messages"

    def get_headers(self, api_key: str) -> dict:
        return {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

    def build_request_payload(self, req: NormalizedRequest) -> dict:
        payload: dict = {
            "model": req.model,
            "messages": req.messages,
            "max_tokens": req.max_tokens or 4096,
        }
        if req.system:
            payload["system"] = req.system
        if req.temperature is not None:
            payload["temperature"] = req.temperature
        if req.tools:
            payload["tools"] = req.tools  # Already in Anthropic format

        return payload

    def parse_response(self, data: dict) -> NormalizedResponse:
        usage = data.get("usage", {})
        content_blocks = data.get("content", [])
        stop_reason = data.get("stop_reason", "end_turn")

        text_parts = []
        tool_calls = []

        for block in content_blocks:
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.get("id", ""),
                        name=block.get("name", ""),
                        input=block.get("input", {}),
                    )
                )

        finish_reason = "tool_use" if tool_calls else (
            "stop" if stop_reason in ("end_turn", "stop_sequence") else stop_reason
        )

        return NormalizedResponse(
            content="\n".join(text_parts) or None,
            tool_calls=tool_calls,
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            finish_reason=finish_reason,
            raw_meta={"id": data.get("id"), "model": data.get("model")},
        )

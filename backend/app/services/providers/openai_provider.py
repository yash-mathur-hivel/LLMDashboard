from app.services.providers.base import BaseProvider, NormalizedRequest, NormalizedResponse, ToolCall


class OpenAIProvider(BaseProvider):
    def get_api_url(self, model: str) -> str:
        return "https://api.openai.com/v1/chat/completions"

    def get_headers(self, api_key: str) -> dict:
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def build_request_payload(self, req: NormalizedRequest) -> dict:
        messages = []
        if req.system:
            messages.append({"role": "system", "content": req.system})
        messages.extend(req.messages)

        payload: dict = {"model": req.model, "messages": messages}
        if req.max_tokens is not None:
            payload["max_tokens"] = req.max_tokens
        if req.temperature is not None:
            payload["temperature"] = req.temperature

        if req.tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t.get("description", ""),
                        "parameters": t.get("input_schema", t.get("parameters", {})),
                    },
                }
                for t in req.tools
            ]

        return payload

    def parse_response(self, data: dict) -> NormalizedResponse:
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        usage = data.get("usage", {})

        content = message.get("content")
        finish_reason = choice.get("finish_reason", "stop")

        tool_calls = []
        for tc in message.get("tool_calls") or []:
            import json
            args = tc["function"].get("arguments", "{}")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            tool_calls.append(
                ToolCall(
                    id=tc.get("id", ""),
                    name=tc["function"]["name"],
                    input=args,
                )
            )

        return NormalizedResponse(
            content=content,
            tool_calls=tool_calls,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            finish_reason="tool_use" if tool_calls else finish_reason,
            raw_meta={"id": data.get("id"), "model": data.get("model")},
        )


class OpenAICompatibleProvider(OpenAIProvider):
    def __init__(self, api_endpoint: str):
        self._api_endpoint = api_endpoint

    def get_api_url(self, model: str) -> str:
        return self._api_endpoint

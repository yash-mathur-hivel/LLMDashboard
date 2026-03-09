from app.services.providers.base import BaseProvider, NormalizedRequest, NormalizedResponse, ToolCall


class GeminiProvider(BaseProvider):
    def get_api_url(self, model: str) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def get_headers(self, api_key: str) -> dict:
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        }

    def build_request_payload(self, req: NormalizedRequest) -> dict:
        # Convert messages: assistant → model role
        contents = []
        for msg in req.messages:
            role = "model" if msg["role"] == "assistant" else msg["role"]
            content = msg["content"]
            if isinstance(content, str):
                parts = [{"text": content}]
            elif isinstance(content, list):
                parts = content
            else:
                parts = [{"text": str(content)}]
            contents.append({"role": role, "parts": parts})

        payload: dict = {"contents": contents}

        if req.system:
            payload["system_instruction"] = {"parts": [{"text": req.system}]}

        generation_config = {}
        if req.max_tokens:
            generation_config["maxOutputTokens"] = req.max_tokens
        if req.temperature is not None:
            generation_config["temperature"] = req.temperature
        if generation_config:
            payload["generationConfig"] = generation_config

        if req.tools:
            # Convert Anthropic-style tools to Gemini function declarations
            payload["tools"] = [
                {
                    "function_declarations": [
                        {
                            "name": t["name"],
                            "description": t.get("description", ""),
                            "parameters": t.get("input_schema", {}),
                        }
                        for t in req.tools
                    ]
                }
            ]

        return payload

    def parse_response(self, data: dict) -> NormalizedResponse:
        usage = data.get("usageMetadata", {})
        candidates = data.get("candidates", [{}])
        candidate = candidates[0] if candidates else {}
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        finish_reason_raw = candidate.get("finishReason", "STOP")

        text_parts = []
        tool_calls = []

        for part in parts:
            if "text" in part:
                text_parts.append(part["text"])
            elif "functionCall" in part:
                fc = part["functionCall"]
                tool_calls.append(
                    ToolCall(
                        id=fc.get("name", ""),  # Gemini doesn't provide a separate ID
                        name=fc.get("name", ""),
                        input=fc.get("args", {}),
                    )
                )

        finish_map = {
            "STOP": "stop",
            "MAX_TOKENS": "length",
            "SAFETY": "error",
            "RECITATION": "error",
        }
        finish_reason = "tool_use" if tool_calls else finish_map.get(finish_reason_raw, "stop")

        return NormalizedResponse(
            content="\n".join(text_parts) or None,
            tool_calls=tool_calls,
            prompt_tokens=usage.get("promptTokenCount", 0),
            completion_tokens=usage.get("candidatesTokenCount", 0),
            finish_reason=finish_reason,
            raw_meta={"model": data.get("modelVersion")},
        )

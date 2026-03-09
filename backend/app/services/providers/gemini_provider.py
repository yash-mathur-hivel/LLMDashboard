import json

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
                normalized_parts = []
                for item in content:
                    # Simple normalization: support strings and { "type": "text", "text": ... }
                    if isinstance(item, str):
                        normalized_parts.append({"text": item})
                    elif isinstance(item, dict):
                        if "text" in item:
                            normalized_parts.append({"text": item["text"]})
                        elif item.get("type") == "text" and "text" in item:
                            normalized_parts.append({"text": item["text"]})
                        else:
                            # Fallback to string representation for unsupported shapes
                            normalized_parts.append({"text": str(item)})
                    else:
                        normalized_parts.append({"text": str(item)})
                parts = normalized_parts
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
            # Convert tools to Gemini function declarations, supporting both Anthropic-style and OpenAI-style schemas
            payload["tools"] = [
                {
                    "function_declarations": [
                        {
                            "name": t["name"],
                            "description": t.get("description", ""),
                            "parameters": t.get("input_schema") or t.get("parameters") or {},
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
                raw_args = fc.get("arguments", fc.get("args", {}))
                # Gemini often returns arguments as a JSON string; try to parse it
                if isinstance(raw_args, str):
                    try:
                        parsed_args = json.loads(raw_args)
                    except json.JSONDecodeError:
                        parsed_args = {"_raw": raw_args}
                else:
                    parsed_args = raw_args
                tool_calls.append(
                    ToolCall(
                        id=fc.get("name", ""),  # Gemini doesn't provide a separate ID
                        name=fc.get("name", ""),
                        input=parsed_args,
                    )
                )

        finish_map = {
            "STOP": "stop",
            "MAX_TOKENS": "length",
            "SAFETY": "error",
            "RECITATION": "error",
        }
        # Preserve provider finish reason, defaulting to "stop" if unknown
        finish_reason = finish_map.get(finish_reason_raw, "stop")

        return NormalizedResponse(
            content="\n".join(text_parts) or None,
            tool_calls=tool_calls,
            prompt_tokens=usage.get("promptTokenCount", 0),
            completion_tokens=usage.get("candidatesTokenCount", 0),
            finish_reason=finish_reason,
            raw_meta={
                "model": data.get("modelVersion"),
                "finish_reason_raw": finish_reason_raw,
                "candidates": data.get("candidates"),
                "safety_ratings": data.get("promptFeedback", {}).get("safetyRatings"),
            },
        )

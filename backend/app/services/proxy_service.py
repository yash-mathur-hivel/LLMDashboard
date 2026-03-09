import uuid
import time
from dataclasses import asdict

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request_log import RequestLog
from app.services.providers.base import NormalizedRequest, NormalizedResponse
from app.services.providers.openai_provider import OpenAIProvider, OpenAICompatibleProvider
from app.services.providers.anthropic_provider import AnthropicProvider
from app.services.providers.gemini_provider import GeminiProvider
from app.services.providers.azure_provider import AzureProvider
from app.services.cost_service import calculate_cost
from app.utils.key_masker import mask_api_key
from app.utils.domain_extractor import extract_domain


def detect_provider(model: str, api_endpoint: str | None) -> str:
    if api_endpoint:
        return "openai_compatible"
    model_lower = model.lower()
    if any(model_lower.startswith(p) for p in ("gpt-", "o1", "o3")):
        return "openai"
    if model_lower.startswith("claude-"):
        return "anthropic"
    if model_lower.startswith("gemini-"):
        return "gemini"
    return "openai_compatible"


def get_provider(provider_name: str, api_endpoint: str | None):
    if provider_name == "openai":
        return OpenAIProvider()
    if provider_name == "anthropic":
        return AnthropicProvider()
    if provider_name == "gemini":
        return GeminiProvider()
    if provider_name == "azure":
        return AzureProvider(api_endpoint or "")
    return OpenAICompatibleProvider(api_endpoint or "")


async def execute_proxy(
    *,
    model: str,
    api_key: str,
    provider_override: str | None,
    api_endpoint: str | None,
    label: str | None,
    mcp_config_id: uuid.UUID | None,
    system: str | None,
    messages: list[dict],
    tools: list[dict] | None,
    max_tokens: int | None,
    temperature: float | None,
    referer: str | None,
    origin: str | None,
    db: AsyncSession,
) -> dict:
    provider_name = provider_override or detect_provider(model, api_endpoint)
    provider = get_provider(provider_name, api_endpoint)

    norm_req = NormalizedRequest(
        model=model,
        messages=messages,
        system=system,
        tools=tools,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    payload = provider.build_request_payload(norm_req)
    headers = provider.get_headers(api_key)
    # Ensure custom API endpoints are respected for compatible/azure providers
    if api_endpoint is not None:
        url = api_endpoint
    else:
        url = provider.get_api_url(model)

    masked_key = mask_api_key(api_key)
    origin_domain = extract_domain(referer, origin)

    log_id = uuid.uuid4()
    start_time = time.monotonic()

    status = "success"
    error_message = None
    http_status_code = None
    norm_resp: NormalizedResponse | None = None
    response_data: dict = {}

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            http_status_code = resp.status_code
            try:
                response_data = resp.json()
            except ValueError:
                # Fallback for non-JSON responses
                response_data = {"raw_text": resp.text}

            if resp.status_code >= 400:
                status = "error"
                error_message = str(response_data)
            else:
                norm_resp = provider.parse_response(response_data)
    except httpx.HTTPError as exc:
         status = "error"
         error_message = str(exc)
         # Use a sentinel status code to indicate a transport-level error
         http_status_code = http_status_code or 0
     except Exception:
         # Re-raise unexpected exceptions so they are visible to callers/monitoring
         raise

    latency_ms = int((time.monotonic() - start_time) * 1000)

    prompt_tokens = norm_resp.prompt_tokens if norm_resp is not None else None
    completion_tokens = norm_resp.completion_tokens if norm_resp is not None else None
    cost_usd = calculate_cost(model, prompt_tokens or 0, completion_tokens or 0) if norm_resp is not None else 0.0

    tool_calls_data = None
    if norm_resp and norm_resp.tool_calls:
        tool_calls_data = [
            {"id": tc.id, "name": tc.name, "input": tc.input}
            for tc in norm_resp.tool_calls
        ]

    log = RequestLog(
        id=log_id,
        provider=provider_name,
        model=model,
        masked_api_key=masked_key,
        label=label,
        origin_domain=origin_domain,
        latency_ms=latency_ms,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cost_usd=cost_usd,
        system_prompt=system,
        messages=messages,
        tool_definitions=tools,
        assistant_response=norm_resp.content if norm_resp else None,
        tool_calls=tool_calls_data,
        finish_reason=norm_resp.finish_reason if norm_resp else "error",
        status=status,
        error_message=error_message,
        http_status_code=http_status_code,
        mcp_config_id=mcp_config_id,
        raw_response_meta=norm_resp.raw_meta if norm_resp else response_data,
        )

    db.add(log)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return {
        "log_id": str(log_id),
        "provider": provider_name,
        "model": model,
        "content": norm_resp.content if norm_resp else None,
        "tool_calls": tool_calls_data,
        "finish_reason": norm_resp.finish_reason if norm_resp else "error",
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cost_usd": cost_usd,
        "latency_ms": latency_ms,
        "status": status,
        "error_message": error_message,
        "http_status_code": http_status_code,
        }

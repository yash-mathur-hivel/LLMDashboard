from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.proxy import ProxyRequest, ProxyResponse
from app.services.proxy_service import execute_proxy

router = APIRouter(prefix="/api/proxy", tags=["proxy"])


@router.post("", response_model=ProxyResponse)
async def proxy_request(
    body: ProxyRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    messages = [*body.messages, {"role": "user", "content": body.user_message}]

    result = await execute_proxy(
        model=body.model,
        api_key=body.api_key,
        provider_override=body.provider,
        api_endpoint=body.api_endpoint,
        label=body.label,
        mcp_config_id=body.mcp_config_id,
        system=body.system,
        messages=messages,
        tools=body.tools,
        max_tokens=body.max_tokens,
        temperature=body.temperature,
        referer=request.headers.get("referer"),
        origin=request.headers.get("origin"),
        db=db,
    )
    return result

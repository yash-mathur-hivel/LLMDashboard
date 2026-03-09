import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.mcp_config import MCPServer
from app.schemas.mcp_config import MCPServerCreate, MCPServerUpdate, MCPServerResponse

router = APIRouter(prefix="/api/mcp", tags=["mcp"])


@router.get("", response_model=list[MCPServerResponse])
async def list_servers(db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(MCPServer).order_by(MCPServer.created_at))).scalars().all()
    return [MCPServerResponse.model_validate(r) for r in rows]


@router.post("", response_model=MCPServerResponse, status_code=201)
async def create_server(body: MCPServerCreate, db: AsyncSession = Depends(get_db)):
    server = MCPServer(**body.model_dump())
    db.add(server)
    await db.commit()
    await db.refresh(server)
    return MCPServerResponse.model_validate(server)


@router.put("/{server_id}", response_model=MCPServerResponse)
async def update_server(
    server_id: uuid.UUID, body: MCPServerUpdate, db: AsyncSession = Depends(get_db)
):
    server = await db.get(MCPServer, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="MCP server not found")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(server, k, v)
    await db.commit()
    await db.refresh(server)
    return MCPServerResponse.model_validate(server)


@router.delete("/{server_id}", status_code=204)
async def delete_server(server_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    server = await db.get(MCPServer, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="MCP server not found")
    await db.delete(server)
    await db.commit()


@router.patch("/{server_id}/toggle", response_model=MCPServerResponse)
async def toggle_server(server_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    server = await db.get(MCPServer, server_id)
    if not server:
        raise HTTPException(status_code=404, detail="MCP server not found")
    server.enabled = not server.enabled
    await db.commit()
    await db.refresh(server)
    return MCPServerResponse.model_validate(server)

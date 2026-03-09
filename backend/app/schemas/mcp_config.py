import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel


class MCPServerBase(BaseModel):
    name: str
    transport: str
    command: str | None = None
    args: list[str] | None = None
    url: str | None = None
    headers: dict[str, str] | None = None
    env_vars: dict[str, str] | None = None
    enabled: bool = True


class MCPServerCreate(MCPServerBase):
    pass


class MCPServerUpdate(MCPServerBase):
    pass


class MCPServerResponse(MCPServerBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

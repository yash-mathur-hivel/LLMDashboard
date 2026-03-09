import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base


class MCPServer(Base):
    __tablename__ = "mcp_servers"
    __table_args__ = {"schema": "llm_monitoring"}

    id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    transport: Mapped[str] = mapped_column(String(20), nullable=False)
    command: Mapped[str | None] = mapped_column(Text)
    args: Mapped[list[str] | None] = mapped_column(JSONB)
    url: Mapped[str | None] = mapped_column(Text)
    headers: Mapped[dict | None] = mapped_column(JSONB)
    env_vars: Mapped[dict | None] = mapped_column(JSONB)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    request_logs: Mapped[list["RequestLog"]] = relationship(back_populates="mcp_server")

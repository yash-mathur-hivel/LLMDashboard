import uuid
from datetime import datetime
from sqlalchemy import (
    String, Integer, Text, Boolean, DateTime, SmallInteger,
    ForeignKey, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, NUMERIC
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base


class RequestLog(Base):
    __tablename__ = "request_logs"
    __table_args__ = (
        Index("ix_request_logs_requested_at", "requested_at"),
        Index("ix_request_logs_provider", "provider"),
        Index("ix_request_logs_model", "model"),
        Index("ix_request_logs_masked_api_key", "masked_api_key"),
        Index("ix_request_logs_origin_domain", "origin_domain"),
        Index("ix_request_logs_label", "label"),
        Index("ix_request_logs_status", "status"),
        {"schema": "llm_monitoring"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    masked_api_key: Mapped[str | None] = mapped_column(String(30))
    label: Mapped[str | None] = mapped_column(String(255))
    origin_domain: Mapped[str | None] = mapped_column(String(255))
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    prompt_tokens: Mapped[int | None] = mapped_column(Integer)
    completion_tokens: Mapped[int | None] = mapped_column(Integer)
    cost_usd: Mapped["Decimal | None"] = mapped_column(NUMERIC(12, 8))
    system_prompt: Mapped[str | None] = mapped_column(Text)
    messages: Mapped[dict] = mapped_column(JSONB, nullable=False)
    tool_definitions: Mapped[dict | None] = mapped_column(JSONB)
    assistant_response: Mapped[str | None] = mapped_column(Text)
    tool_calls: Mapped[dict | None] = mapped_column(JSONB)
    finish_reason: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="success")
    error_message: Mapped[str | None] = mapped_column(Text)
    http_status_code: Mapped[int | None] = mapped_column(SmallInteger)
    mcp_config_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("llm_monitoring.mcp_servers.id", ondelete="SET NULL"),
    )
    raw_response_meta: Mapped[dict | None] = mapped_column(JSONB)

    mcp_server: Mapped["MCPServer | None"] = relationship(back_populates="request_logs")

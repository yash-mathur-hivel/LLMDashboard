"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-03-08

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS llm_monitoring")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "mcp_servers",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("transport", sa.String(20), nullable=False),
        sa.Column("command", sa.Text(), nullable=True),
        sa.Column("args", postgresql.JSONB(), nullable=True),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("headers", postgresql.JSONB(), nullable=True),
        sa.Column("env_vars", postgresql.JSONB(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        schema="llm_monitoring",
    )

    op.create_table(
        "request_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider", sa.String(50), nullable=False),
        sa.Column("model", sa.String(100), nullable=False),
        sa.Column("masked_api_key", sa.String(30), nullable=True),
        sa.Column("label", sa.String(255), nullable=True),
        sa.Column("origin_domain", sa.String(255), nullable=True),
        sa.Column(
            "requested_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("latency_ms", sa.Integer(), nullable=True),
        sa.Column("prompt_tokens", sa.Integer(), nullable=True),
        sa.Column("completion_tokens", sa.Integer(), nullable=True),
        sa.Column("cost_usd", sa.Numeric(12, 8), nullable=True),
        sa.Column("system_prompt", sa.Text(), nullable=True),
        sa.Column("messages", postgresql.JSONB(), nullable=False),
        sa.Column("tool_definitions", postgresql.JSONB(), nullable=True),
        sa.Column("assistant_response", sa.Text(), nullable=True),
        sa.Column("tool_calls", postgresql.JSONB(), nullable=True),
        sa.Column("finish_reason", sa.String(50), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="success"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("http_status_code", sa.SmallInteger(), nullable=True),
        sa.Column(
            "mcp_config_id",
            postgresql.UUID(as_uuid=True),
            nullable=True,
        ),
        sa.Column("raw_response_meta", postgresql.JSONB(), nullable=True),
        sa.ForeignKeyConstraint(
            ["mcp_config_id"],
            ["llm_monitoring.mcp_servers.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="llm_monitoring",
    )

    op.create_index(
        "ix_request_logs_requested_at",
        "request_logs",
        ["requested_at"],
        schema="llm_monitoring",
    )
    op.create_index(
        "ix_request_logs_provider",
        "request_logs",
        ["provider"],
        schema="llm_monitoring",
    )
    op.create_index(
        "ix_request_logs_model",
        "request_logs",
        ["model"],
        schema="llm_monitoring",
    )
    op.create_index(
        "ix_request_logs_masked_api_key",
        "request_logs",
        ["masked_api_key"],
        schema="llm_monitoring",
    )
    op.create_index(
        "ix_request_logs_origin_domain",
        "request_logs",
        ["origin_domain"],
        schema="llm_monitoring",
    )
    op.create_index(
        "ix_request_logs_label",
        "request_logs",
        ["label"],
        schema="llm_monitoring",
    )
    op.create_index(
        "ix_request_logs_status",
        "request_logs",
        ["status"],
        schema="llm_monitoring",
    )


def downgrade() -> None:
    op.drop_table("request_logs", schema="llm_monitoring")
    op.drop_table("mcp_servers", schema="llm_monitoring")
    op.execute("DROP SCHEMA IF EXISTS llm_monitoring CASCADE")

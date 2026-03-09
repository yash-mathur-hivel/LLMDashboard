from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


VALID_GROUP_BY = {"model", "provider", "masked_api_key", "origin_domain", "label"}
VALID_GRANULARITY = {"hour", "day", "week"}


async def get_summary(
    db: AsyncSession,
    start_date: datetime | None,
    end_date: datetime | None,
    group_by: str | None,
) -> dict:
    where_clauses = ["1=1"]
    params: dict = {}

    if start_date:
        where_clauses.append("requested_at >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where_clauses.append("requested_at <= :end_date")
        params["end_date"] = end_date

    where = " AND ".join(where_clauses)

    # Totals
    totals_sql = text(f"""
        SELECT
            COUNT(*) AS total_requests,
            SUM(prompt_tokens) AS total_prompt_tokens,
            SUM(completion_tokens) AS total_completion_tokens,
            SUM(cost_usd) AS total_cost_usd,
            AVG(latency_ms) AS avg_latency_ms,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY latency_ms) AS p50_latency_ms,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms) AS p95_latency_ms,
            COUNT(*) FILTER (WHERE status = 'error') AS error_count
        FROM llm_monitoring.request_logs
        WHERE {where}
    """)
    totals_row = (await db.execute(totals_sql, params)).mappings().one()

    breakdown = []
    if group_by and group_by in VALID_GROUP_BY:
        breakdown_sql = text(f"""
            SELECT
                {group_by} AS dimension,
                COUNT(*) AS total_requests,
                SUM(prompt_tokens) AS total_prompt_tokens,
                SUM(completion_tokens) AS total_completion_tokens,
                SUM(cost_usd) AS total_cost_usd,
                AVG(latency_ms) AS avg_latency_ms
            FROM llm_monitoring.request_logs
            WHERE {where}
            GROUP BY {group_by}
            ORDER BY total_requests DESC
            LIMIT 50
        """)
        rows = (await db.execute(breakdown_sql, params)).mappings().all()
        breakdown = [dict(r) for r in rows]

    return {
        "total_requests": totals_row["total_requests"] or 0,
        "total_prompt_tokens": int(totals_row["total_prompt_tokens"] or 0),
        "total_completion_tokens": int(totals_row["total_completion_tokens"] or 0),
        "total_cost_usd": float(totals_row["total_cost_usd"] or 0),
        "avg_latency_ms": float(totals_row["avg_latency_ms"] or 0),
        "p50_latency_ms": float(totals_row["p50_latency_ms"] or 0),
        "p95_latency_ms": float(totals_row["p95_latency_ms"] or 0),
        "error_count": int(totals_row["error_count"] or 0),
        "breakdown": breakdown,
    }


async def get_timeseries(
    db: AsyncSession,
    start_date: datetime | None,
    end_date: datetime | None,
    granularity: str,
    group_by: str | None,
) -> list[dict]:
    if granularity not in VALID_GRANULARITY:
        granularity = "day"

    where_clauses = ["1=1"]
    params: dict = {}
    if start_date:
        where_clauses.append("requested_at >= :start_date")
        params["start_date"] = start_date
    if end_date:
        where_clauses.append("requested_at <= :end_date")
        params["end_date"] = end_date
    where = " AND ".join(where_clauses)

    if group_by and group_by in VALID_GROUP_BY:
        sql = text(f"""
            SELECT
                DATE_TRUNC('{granularity}', requested_at) AS bucket,
                {group_by} AS dimension,
                COUNT(*) AS total_requests,
                SUM(cost_usd) AS total_cost_usd,
                SUM(prompt_tokens) AS total_prompt_tokens,
                SUM(completion_tokens) AS total_completion_tokens,
                AVG(latency_ms) AS avg_latency_ms
            FROM llm_monitoring.request_logs
            WHERE {where}
            GROUP BY bucket, {group_by}
            ORDER BY bucket ASC
        """)
    else:
        sql = text(f"""
            SELECT
                DATE_TRUNC('{granularity}', requested_at) AS bucket,
                COUNT(*) AS total_requests,
                SUM(cost_usd) AS total_cost_usd,
                SUM(prompt_tokens) AS total_prompt_tokens,
                SUM(completion_tokens) AS total_completion_tokens,
                AVG(latency_ms) AS avg_latency_ms
            FROM llm_monitoring.request_logs
            WHERE {where}
            GROUP BY bucket
            ORDER BY bucket ASC
        """)

    rows = (await db.execute(sql, params)).mappings().all()
    def _serialize(v):
        if v is None:
            return None
        if hasattr(v, "isoformat"):
            return v.isoformat()
        if isinstance(v, (int, float)):
            return float(v)
        return v  # strings (dimension) pass through as-is

    return [{k: _serialize(v) for k, v in r.items()} for r in rows]


async def get_dimensions(db: AsyncSession) -> dict:
    sql = text("""
        SELECT
            ARRAY_AGG(DISTINCT provider ORDER BY provider) AS providers,
            ARRAY_AGG(DISTINCT model ORDER BY model) AS models,
            ARRAY_AGG(DISTINCT masked_api_key ORDER BY masked_api_key) AS masked_api_keys,
            ARRAY_AGG(DISTINCT origin_domain ORDER BY origin_domain) AS origin_domains,
            ARRAY_AGG(DISTINCT label ORDER BY label) AS labels
        FROM llm_monitoring.request_logs
    """)
    row = (await db.execute(sql)).mappings().one()

    def clean(arr):
        if arr is None:
            return []
        cleaned = []
        for x in arr:
            if x is None:
                continue
            if isinstance(x, str):
                if x.strip() == "":
                    continue
                cleaned.append(x.strip())
            else:
                cleaned.append(x)
        return cleaned

    return {
        "providers": clean(row["providers"]),
        "models": clean(row["models"]),
        "masked_api_keys": clean(row["masked_api_keys"]),
        "origin_domains": clean(row["origin_domains"]),
        "labels": clean(row["labels"]),
    }

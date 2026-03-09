import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, or_, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.request_log import RequestLog
from app.schemas.request_log import RequestLogDetail, RequestLogListItem, LogsResponse

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.get("", response_model=LogsResponse)
async def list_logs(
    provider: str | None = Query(None),
    model: str | None = Query(None),
    masked_api_key: str | None = Query(None),
    origin_domain: str | None = Query(None),
    label: str | None = Query(None),
    status: str | None = Query(None),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    q = select(RequestLog)

    if provider:
        q = q.where(RequestLog.provider == provider)
    if model:
        q = q.where(RequestLog.model == model)
    if masked_api_key:
        q = q.where(RequestLog.masked_api_key == masked_api_key)
    if origin_domain:
        q = q.where(RequestLog.origin_domain == origin_domain)
    if label:
        q = q.where(RequestLog.label == label)
    if status:
        q = q.where(RequestLog.status == status)
    if start_date:
        q = q.where(RequestLog.requested_at >= start_date)
    if end_date:
        q = q.where(RequestLog.requested_at <= end_date)
    if search:
        q = q.where(
            or_(
                RequestLog.model.ilike(f"%{search}%"),
                RequestLog.label.ilike(f"%{search}%"),
                RequestLog.origin_domain.ilike(f"%{search}%"),
                cast(RequestLog.assistant_response, String).ilike(f"%{search}%"),
            )
        )

    count_q = select(func.count()).select_from(q.subquery())
    total = (await db.execute(count_q)).scalar() or 0

    q = q.order_by(RequestLog.requested_at.desc())
    q = q.offset((page - 1) * page_size).limit(page_size)

    rows = (await db.execute(q)).scalars().all()

    return LogsResponse(
        items=[RequestLogListItem.model_validate(r) for r in rows],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=0 if total == 0 else -(-total // page_size),
    )


@router.get("/{log_id}", response_model=RequestLogDetail)
async def get_log(log_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    row = await db.get(RequestLog, log_id)
    if not row:
        raise HTTPException(status_code=404, detail="Log not found")
    return RequestLogDetail.model_validate(row)

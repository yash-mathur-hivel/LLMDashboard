from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.analytics import SummaryResponse, TimeseriesResponse, DimensionsResponse
from app.services import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary", response_model=SummaryResponse)
async def summary(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    group_by: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await analytics_service.get_summary(db, start_date, end_date, group_by)


@router.get("/timeseries", response_model=TimeseriesResponse)
async def timeseries(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    granularity: str = Query("day"),
    group_by: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    data = await analytics_service.get_timeseries(db, start_date, end_date, granularity, group_by)
    return TimeseriesResponse(data=data)


@router.get("/dimensions", response_model=DimensionsResponse)
async def dimensions(db: AsyncSession = Depends(get_db)):
    return await analytics_service.get_dimensions(db)

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.db.session import get_db
from app.schemas.analytics import (
    SummaryResponse, CategoryBreakdownResponse, 
    MonthlyTrendResponse, TopMerchantResponse
)
from app.services.analytics import (
    get_summary, get_category_breakdown, 
    get_monthly_trends, get_top_merchants
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/summary", response_model=SummaryResponse)
def get_analytics_summary(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Aggregate high-level transaction statistics."""
    return get_summary(db, start_date=start_date, end_date=end_date)

@router.get("/category-breakdown", response_model=CategoryBreakdownResponse)
def get_analytics_category_breakdown(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get category-wise spending totals (Completed transactions only)."""
    items = get_category_breakdown(db, start_date=start_date, end_date=end_date)
    return CategoryBreakdownResponse(items=items)

@router.get("/monthly-trends", response_model=MonthlyTrendResponse)
def get_analytics_monthly_trends(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get month-over-month total spending (Completed transactions only)."""
    items = get_monthly_trends(db, start_date=start_date, end_date=end_date)
    return MonthlyTrendResponse(items=items)

@router.get("/top-merchants", response_model=TopMerchantResponse)
def get_analytics_top_merchants(
    limit: int = Query(10, description="Number of top merchants to return"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get top recipients ordered by total spend (Completed transactions only)."""
    items = get_top_merchants(db, limit=limit, start_date=start_date, end_date=end_date)
    return TopMerchantResponse(items=items)

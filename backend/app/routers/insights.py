import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.rule_insights import (
    get_monthly_insights,
    get_savings_insights,
    get_summary_insights,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/monthly")
def monthly_insights(db: Session = Depends(get_db)):
    """Rule-based monthly spending insights."""
    try:
        return get_monthly_insights(db)
    except Exception as e:
        logger.exception("Monthly insights failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/savings")
def savings_insights(db: Session = Depends(get_db)):
    """Rule-based savings recommendations."""
    try:
        return get_savings_insights(db)
    except Exception as e:
        logger.exception("Savings insights failed")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary")
def summary_insights(db: Session = Depends(get_db)):
    """Rule-based dashboard summary."""
    try:
        return get_summary_insights(db)
    except Exception as e:
        logger.exception("Summary insights failed")
        raise HTTPException(status_code=500, detail=str(e))

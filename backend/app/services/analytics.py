from sqlalchemy.orm import Session
from sqlalchemy import func, desc, nullslast
from typing import Optional, List, Dict, Any
from datetime import date

from app.models.db_models import Transaction

def apply_base_filters(
    query, 
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None,
    category: Optional[str] = None
):
    """Applies common optional filters to any transaction query."""
    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)
    if category:
        query = query.filter(Transaction.category == category)
    return query

def apply_spend_filters(query, exclude_self_transfer: bool = True):
    """
    Applies strict analytics filters ensuring only valid 'Completed'
    transactions count towards spend aggregates.
    """
    query = query.filter(Transaction.status == "Completed")
    if exclude_self_transfer:
        query = query.filter(Transaction.transaction_type != "Self Transfer")
    return query

def get_summary(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict[str, Any]:
    base_q = apply_base_filters(db.query(Transaction), start_date, end_date)
    
    # Status metrics
    total_tx = base_q.count()
    completed = base_q.filter(Transaction.status == "Completed").count()
    pending = base_q.filter(Transaction.status == "Pending").count()
    failed = base_q.filter(Transaction.status == "Failed").count()
    
    # Spend metrics
    completed_q = base_q.filter(Transaction.status == "Completed")
    total_spend = completed_q.with_entities(func.sum(Transaction.amount)).scalar() or 0.0
    
    completed_no_self_q = completed_q.filter(Transaction.transaction_type != "Self Transfer")
    total_spend_no_self = completed_no_self_q.with_entities(func.sum(Transaction.amount)).scalar() or 0.0
    
    avg_no_self = completed_no_self_q.with_entities(func.avg(Transaction.amount)).scalar() or 0.0
    avg_inc_self = completed_q.with_entities(func.avg(Transaction.amount)).scalar() or 0.0
    
    # Date bounds
    min_date = base_q.with_entities(func.min(Transaction.transaction_date)).scalar()
    max_date = base_q.with_entities(func.max(Transaction.transaction_date)).scalar()
    
    return {
        "total_transactions": total_tx,
        "completed_transactions": completed,
        "pending_transactions": pending,
        "failed_transactions": failed,
        "total_completed_spend": float(total_spend),
        "total_completed_spend_excluding_self_transfers": float(total_spend_no_self),
        "average_completed_transaction_amount_excluding_self_transfers": float(avg_no_self),
        "average_completed_transaction_amount_including_self_transfers": float(avg_inc_self),
        "date_range": {
            "start_date": min_date,
            "end_date": max_date
        }
    }

def get_category_breakdown(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict[str, Any]]:
    q = apply_base_filters(db.query(Transaction), start_date, end_date)
    q = apply_spend_filters(q, exclude_self_transfer=True)
    
    results = q.with_entities(
        func.coalesce(Transaction.category, "Other").label("norm_category"),
        func.sum(Transaction.amount).label("total_spend"),
        func.count(Transaction.id).label("transaction_count")
    ).group_by(
        func.coalesce(Transaction.category, "Other")
    ).order_by(
        desc("total_spend")
    ).all()
    
    return [
        {
            "category": r.norm_category,
            "total_spend": float(r.total_spend),
            "transaction_count": r.transaction_count
        } for r in results
    ]

def get_monthly_trends(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict[str, Any]]:
    q = apply_base_filters(db.query(Transaction), start_date, end_date)
    q = apply_spend_filters(q, exclude_self_transfer=True)
    
    # Format YYYY-MM
    # SQLite uses strftime
    # Postgres uses to_char, but strftime usually fails on postgres if running hybrid.
    # Since we are using SQLite in the environment, we use strftime.
    # We can also fallback or do it consistently with python formatting if we fetched raw date, but group by requires DB-side formatting.
    # Using func.strftime('%Y-%m', Transaction.transaction_date) for SQLite
    
    month_exp = func.strftime('%Y-%m', Transaction.transaction_date)
    
    results = q.with_entities(
        month_exp.label("month_label"),
        func.sum(Transaction.amount).label("total_spend"),
        func.count(Transaction.id).label("transaction_count")
    ).filter(
        Transaction.transaction_date != None
    ).group_by(
        month_exp
    ).order_by(
        "month_label"
    ).all()
    
    return [
        {
            "month_label": r.month_label or "Unknown",
            "total_spend": float(r.total_spend),
            "transaction_count": r.transaction_count
        } for r in results
    ]

def get_top_merchants(db: Session, limit: int = 10, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict[str, Any]]:
    q = apply_base_filters(db.query(Transaction), start_date, end_date)
    q = apply_spend_filters(q, exclude_self_transfer=True)
    
    # To get merchant name, we group by name
    # We select the MAX(category) as a fallback representation
    results = q.with_entities(
        Transaction.name,
        func.coalesce(func.max(Transaction.category), "Other").label("category"),
        func.sum(Transaction.amount).label("total_spend"),
        func.count(Transaction.id).label("transaction_count")
    ).group_by(
        Transaction.name
    ).order_by(
        desc("total_spend")
    ).limit(limit).all()
    
    return [
        {
            "merchant_name": r.name,
            "category": r.category,
            "total_spend": float(r.total_spend),
            "transaction_count": r.transaction_count
        } for r in results
    ]

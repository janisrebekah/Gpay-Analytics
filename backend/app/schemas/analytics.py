from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class DateRange(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class SummaryResponse(BaseModel):
    total_transactions: int
    completed_transactions: int
    pending_transactions: int
    failed_transactions: int
    total_completed_spend: float
    total_completed_spend_excluding_self_transfers: float
    average_completed_transaction_amount_excluding_self_transfers: float
    average_completed_transaction_amount_including_self_transfers: float
    date_range: DateRange

class CategoryBreakdownItem(BaseModel):
    category: str
    total_spend: float
    transaction_count: int

class CategoryBreakdownResponse(BaseModel):
    items: List[CategoryBreakdownItem]

class MonthlyTrendItem(BaseModel):
    month_label: str  # e.g., "2026-01"
    total_spend: float
    transaction_count: int

class MonthlyTrendResponse(BaseModel):
    items: List[MonthlyTrendItem]

class TopMerchantItem(BaseModel):
    merchant_name: str
    category: str
    total_spend: float
    transaction_count: int

class TopMerchantResponse(BaseModel):
    items: List[TopMerchantItem]

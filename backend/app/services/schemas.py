from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import datetime

class NormalizedTransaction(BaseModel):
    """
    Schema for a parsed and normalized Google Pay transaction.
    """
    name: str = Field(..., description="Standardized merchant or recipient name")
    amount: float = Field(..., description="Numeric amount paid in INR")
    transaction_date: Optional[str] = Field(None, description="Transaction date in YYYY-MM-DD format")
    month: Optional[int] = Field(None, description="Month of the transaction (1-12)")
    year: Optional[int] = Field(None, description="Year of the transaction")
    day_of_week: Optional[str] = Field(None, description="Day of the week (e.g., Monday)")
    transaction_type: str = Field(..., description="Type of transaction (e.g., Merchant, P2P, Transfer)")
    category: str | None = Field(default=None, description="Spending category")
    status: str = Field(..., description="Transaction status (e.g., Completed, Failed)")
    
    # Original data retained for debugging and AI pipelines
    date_raw: str = Field(..., description="Raw date string from the HTML")
    raw_text: str = Field(..., description="Raw text extracted from the HTML block")
    source: str = Field(..., description="Original source file name")

    model_config = ConfigDict(from_attributes=True)

class GPayTakeoutResponse(BaseModel):
    """
    Response schema for parsing a Google Takeout HTML file.
    """
    total_blocks_scanned: int = Field(..., description="Total number of transaction-like blocks found in the HTML")
    valid_transactions: int = Field(..., description="Number of successfully parsed Google Pay transactions")
    failed_entries: int = Field(..., description="Number of Google Pay blocks that could not be parsed")
    saved_transactions_count: int = Field(0, description="Number of new transactions saved to Database (duplicates ignored)")
    parsed_transactions: List[NormalizedTransaction] = Field(..., description="List of successfully parsed transactions")

import re
import logging
from datetime import datetime
from typing import Dict, Any

from app.services.classifier import determine_category

logger = logging.getLogger(__name__)

def clean_merchant_name(name: str) -> str:
    """Standardizes merchant names by cleaning extra spaces and noisy text."""
    # Remove multiple spaces, newlines, and strip
    cleaned_name = re.sub(r'\s+', ' ', name).strip()
    return cleaned_name

def _is_self_transfer(name_lower: str, raw_lower: str) -> bool:
    """Check for self or direct transfers originating to own account."""
    keywords = ["self", "direct transfer"]
    if any(k in name_lower or k in raw_lower for k in keywords):
        return True
    if "using bank account" in raw_lower and "to " not in raw_lower:
        return True
    return False

def _is_bill_payment(name_lower: str, raw_lower: str) -> bool:
    """Check for predictable automated bills, utility recharge, and telecom companies."""
    keywords = [
        "airtel", "jio", "recharge", "prepaid", "broadband", 
        "electricity", "dth", "payments bank", "bill"
    ]
    return any(k in name_lower or k in raw_lower for k in keywords)

def _is_merchant_payment(name_lower: str, raw_lower: str) -> bool:
    """Check for registered businesses, stores, and institutions."""
    keywords = [
        "bakery", "store", "supermarket", "institute", "limited", "ltd", 
        "retail", "swiggy", "zudio", "amazon", "cloud", "private limited", 
        "pvt ltd", "merchant", "shop", "technologies", "inc", "llc", ".com",
        "sweet", "restaurant", "mart", "enterprise", "service", "app"
    ]
    # Word boundary checks aren't strictly required for these loud tokens
    return any(k in name_lower or k in raw_lower for k in keywords)

def _is_human_name(name: str) -> bool:
    """
    Heuristic to determine if a string looks like a personal name.
    Permits alphabetic characters, spaces, and periods (initials).
    Rejects strings with numbers or unusual punctuation.
    """
    if name.lower() == "miscellaneous":
        return False
        
    clean_name = name.replace(".", "").replace("'", "")
    # If the remaining string is entirely alphabetic characters and spaces
    if re.match(r'^[A-Za-z\s]+$', clean_name):
        return True
        
    return False

def determine_transaction_type(name: str, raw_text: str) -> str:
    """Categorizes the transaction completely deterministically via rule-based pipelines."""
    name_lower = name.lower()
    raw_lower = raw_text.lower()
    
    if _is_self_transfer(name_lower, raw_lower):
        return "Self Transfer"
        
    if _is_bill_payment(name_lower, raw_lower):
        return "Bill Payment"
        
    if _is_merchant_payment(name_lower, raw_lower):
        return "Merchant Payment"
        
    if _is_human_name(name):
        return "P2P Payment"
        
    return "Miscellaneous"

def parse_date_string(date_raw: str) -> Dict[str, Any]:
    """
    Parses the raw date string into a structured dictionary with:
    - transaction_date: str (YYYY-MM-DD)
    - month: int
    - year: int
    - day_of_week: str
    If parsing fails, returns None for the fields.
    """
    # 1. Clean invisible unicode characters (like narrow no-break space \u202f)
    cleaned_date = re.sub(r'\s+', ' ', date_raw).strip()
    
    # 2. Robustly remove timezone components (IST, GMT, GMT+05:30, GMT-0400, etc.)
    # Match a space, 2-4 uppercase letters, optionally followed by timezone offsets (+05:30)
    cleaned_date = re.sub(r'\s+[A-Z]{2,4}([+-]\d{2}:?\d{2})?$', '', cleaned_date)
    
    # 3. Remove commas to standardize parsing
    cleaned_date = cleaned_date.replace(',', '').strip()
    
    # Add various formats to handle different locales or variations
    formats_to_try = [
        "%b %d %Y %I:%M:%S %p",  # Jan 9 2026 6:06:11 PM
        "%B %d %Y %I:%M:%S %p",  # January 9 2026 6:06:11 PM
        "%d %b %Y %I:%M:%S %p",  # 9 Jan 2026 6:06:11 PM
        "%b %d %Y %H:%M:%S",     # Jan 9 2026 18:06:11
        "%Y-%m-%d %H:%M:%S",     # 2026-01-09 18:06:11
        "%b %d %Y %I:%M %p",     # Fallback without seconds
        "%d %b %Y %I:%M %p"
    ]
    
    dt_obj = None
    for fmt in formats_to_try:
        try:
            dt_obj = datetime.strptime(cleaned_date, fmt)
            break
        except ValueError:
            continue

    if dt_obj is None:
        logger.warning(f"Could not parse datetime from: '{date_raw}' (cleaned: '{cleaned_date}')")
        return {
            "transaction_date": None,
            "month": None,
            "year": None,
            "day_of_week": None
        }
        
    return {
        "transaction_date": dt_obj.strftime("%Y-%m-%d"),
        "month": dt_obj.month,
        "year": dt_obj.year,
        "day_of_week": dt_obj.strftime("%A")
    }

def normalize_transaction(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Combines all normalization steps onto the raw extracted data dictionary."""
    # 1. Standardize merchant name
    name = clean_merchant_name(raw_data.get("name", ""))
    raw_data["name"] = name
    
    # 2. Add transaction type
    raw_data["transaction_type"] = determine_transaction_type(name, raw_data.get("raw_text", ""))
    
    # 3. Parse dates
    date_info = parse_date_string(raw_data.get("date_raw", ""))
    raw_data.update(date_info)
    
    # 4. Add category
    raw_data["category"] = determine_category(
        name=name,
        raw_text=raw_data.get("raw_text", ""),
        transaction_type=raw_data["transaction_type"]
    )
    
    return raw_data

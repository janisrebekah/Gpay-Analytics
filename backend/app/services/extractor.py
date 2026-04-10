import re
import logging
from typing import Optional
from .schemas import NormalizedTransaction
from .normalizer import normalize_transaction

logger = logging.getLogger(__name__)

def extract_transaction_data(text_content: str, original_filename: str) -> Optional[NormalizedTransaction]:
    """
    Extracts and normalizes transaction info from the pipe-separated text content 
    of a Google Pay transaction block.
    
    Args:
        text_content (str): The pipe-separated raw text of the HTML div element.
        original_filename (str): The original name of the uploaded HTML file.
        
    Returns:
        Optional[NormalizedTransaction]: A normalized transaction model or None
    """
    if "Google Pay" not in text_content or "Paid" not in text_content:
        return None

    parts = [p.strip() for p in text_content.split('|') if p.strip()]
    
    if len(parts) < 3:
        logger.debug(f"Transaction block has too few parts: {text_content}")
        return None
        
    try:
        full_text = parts[1]
        date_info = parts[2]
        status = "Failed" if "Failed" in text_content else "Completed"
        
        # --- Robust Regex Extraction ---
        amount_match = re.search(r'₹([\d,.]+)', full_text)
        amount_str = amount_match.group(1).replace(',', '') if amount_match else "0"
        amount = float(amount_str) # ensured to be numeric
        
        name_match = re.search(r'to\s+(.*?)(?=\s+using|\s+[A-Z][a-z]{2}\s+\d|$)', full_text)
        
        if name_match:
            name = name_match.group(1).strip()
        elif "using Bank Account" in full_text and "to" not in full_text:
            name = "Self/Direct Transfer"
        else:
            name = "Miscellaneous"
            
        raw_dict = {
            "name": name,
            "amount": amount,
            "date_raw": date_info,
            "status": status,
            "raw_text": text_content,
            "source": original_filename
        }
        
        # Apply Normalization Pipeline
        normalized_data = normalize_transaction(raw_dict)
        
        return NormalizedTransaction(**normalized_data)
        
    except Exception as e:
        logger.warning(f"Failed to parse transaction block from {original_filename}: {e}. Text: {text_content}")
        return None

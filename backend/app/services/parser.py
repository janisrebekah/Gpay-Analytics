import logging
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Union, Optional

from .schemas import GPayTakeoutResponse
from .extractor import extract_transaction_data

logger = logging.getLogger(__name__)

def parse_google_takeout_html(
    file_path: Union[str, Path], 
    original_filename: Optional[str] = None
) -> GPayTakeoutResponse:
    """
    Parses a Google Takeout 'My Activity.html' file and returns a detailed response.
    
    Args:
        file_path (Union[str, Path]): The path to the 'My Activity.html' file on disk.
        original_filename (Optional[str]): The original filename chosen by the client,
                                          to use in the 'source' field of the output.
        
    Returns:
        GPayTakeoutResponse: Structured results including parsed transactions and stats.
    """
    path_obj = Path(file_path)
    if not path_obj.exists():
        logger.error(f"GPay activity file not found: {path_obj}")
        raise FileNotFoundError(f"File not found: {path_obj}")
        
    # Use source name for extraction reference so original filename is exported
    source_name = original_filename if original_filename else path_obj.name
        
    logger.info(f"Parsing Google Takeout file (mapped to {source_name}): {path_obj}")
    transactions = []
    total_blocks_scanned = 0
    failed_entries = 0
    
    try:
        with open(path_obj, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        # Iterate through each transaction block based on outer-cell class
        for entry in soup.find_all('div', class_='outer-cell'):
            text_content = entry.get_text(separator='|')
            
            # We count only blocks acting like Google Pay Paid instances
            if "Google Pay" in text_content and "Paid" in text_content:
                total_blocks_scanned += 1
                transaction = extract_transaction_data(text_content, original_filename=source_name)
                
                if transaction:
                    transactions.append(transaction)
                else:
                    failed_entries += 1
                
        logger.info(
            f"Extraction complete for {source_name}. "
            f"Scanned: {total_blocks_scanned}, Valid: {len(transactions)}, Failed: {failed_entries}"
        )
        
        return GPayTakeoutResponse(
            total_blocks_scanned=total_blocks_scanned,
            valid_transactions=len(transactions),
            failed_entries=failed_entries,
            parsed_transactions=transactions
        )
        
    except Exception as e:
        logger.error(f"Error parsing HTML file {path_obj}: {e}", exc_info=True)
        raise

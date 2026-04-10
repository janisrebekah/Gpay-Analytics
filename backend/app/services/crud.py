import hashlib
import logging
from typing import List
from sqlalchemy.orm import Session

from app.models.db_models import Upload, Transaction
from app.services.schemas import NormalizedTransaction

logger = logging.getLogger(__name__)

def generate_transaction_hash(t: NormalizedTransaction) -> str:
    """
    Creates a deterministic hash to prevent obvious duplicates based on user requirements.
    Uses: name, amount, date_raw, status
    """
    raw_string = f"{t.name}|{t.amount}|{t.date_raw}|{t.status}"
    return hashlib.sha256(raw_string.encode('utf-8')).hexdigest()

def create_upload_record(db: Session, filename: str, total_scanned: int, valid_count: int, failed_count: int) -> Upload:
    """Save metadata about the incoming HTML file into the uploads table."""
    db_upload = Upload(
        filename=filename,
        total_scanned=total_scanned,
        valid_count=valid_count,
        failed_count=failed_count
    )
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)
    return db_upload

def save_transactions(db: Session, upload_id: int, transactions: List[NormalizedTransaction]) -> int:
    """
    Bulk inserts mapped transactions into the database.
    Uses a database-agnostic methodology to avoid inserting duplicates:
    1. Collect incoming hashes.
    2. Query DB for existing hashes from the incoming set.
    3. Bulk save only the unobserved records.
    """
    if not transactions:
        return 0

    from datetime import datetime

    # 1. Deduplicate the incoming set itself and prepare objects
    incoming_data = {}
    for t in transactions:
        tx_hash = generate_transaction_hash(t)
        if tx_hash not in incoming_data:
            # Safely cast YYYY-MM-DD strings back to SQLAlchemy acceptable actual date objects 
            date_obj = None
            if t.transaction_date:
                try:
                    date_obj = datetime.strptime(t.transaction_date, "%Y-%m-%d").date()
                except ValueError:
                    pass
                    
            incoming_data[tx_hash] = {
                "upload_id": upload_id,
                "transaction_hash": tx_hash,
                "name": t.name,
                "amount": t.amount,
                "transaction_date": date_obj,
                "month": t.month,
                "year": t.year,
                "day_of_week": t.day_of_week,
                "transaction_type": t.transaction_type,
                "category": t.category,
                "status": t.status,
                "date_raw": t.date_raw,
                "raw_text": t.raw_text,
                "source": t.source
            }
            
    # 2. Query DB to determine which hashes already exist
    incoming_hashes = list(incoming_data.keys())
    existing_records = db.query(Transaction.transaction_hash).filter(
        Transaction.transaction_hash.in_(incoming_hashes)
    ).all()
    existing_hashes = {r[0] for r in existing_records}
    
    # 3. Filter out existing records
    new_records = [
        Transaction(**data) 
        for tx_hash, data in incoming_data.items() 
        if tx_hash not in existing_hashes
    ]
    
    if not new_records:
        logger.info(f"Ignored {len(transactions)} entirely duplicated transactions.")
        return 0
        
    try:
        # Use database-agnostic bulk insertion format
        db.bulk_save_objects(new_records)
        db.commit()
        
        saved_count = len(new_records)
        logger.info(f"Saved {saved_count} new transactions (ignored {len(transactions) - saved_count} duplicates).")
        return saved_count
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error bulk saving transactions: {e}", exc_info=True)
        raise

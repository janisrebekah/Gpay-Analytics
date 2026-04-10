import os
import shutil
import logging
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.services.parser import parse_google_takeout_html
from app.services.schemas import GPayTakeoutResponse
from app.db.session import get_db
from app.services.crud import create_upload_record, save_transactions

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["Google Takeout"]
)

# Use a temporary directory for uploads
UPLOAD_DIR = Path("tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload-html", response_model=GPayTakeoutResponse)
async def upload_takeout_html(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a Google Pay Takeout HTML file ('My Activity.html') for parsing.
    The file will be temporarily saved, parsed, automatically persisted, and cleanly removed.
    """
    if not file.filename.endswith(".html"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .html files are allowed."
        )

    temp_file_path = UPLOAD_DIR / f"temp_{file.filename}"
    
    try:
        logger.info(f"Receiving uploaded file: {file.filename}")
        
        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"File saved temporarily to {temp_file_path}")
        
        # Parse the HTML file using our parser logic
        # Pass the original file's name so it stays clean in the DB schema
        result = parse_google_takeout_html(temp_file_path, original_filename=file.filename)
        
        # Save stats to PostgreSQL
        upload_record = create_upload_record(
            db=db,
            filename=file.filename,
            total_scanned=result.total_blocks_scanned,
            valid_count=result.valid_transactions,
            failed_count=result.failed_entries
        )
        
        # Save nested transactions
        saved_count = save_transactions(
            db=db,
            upload_id=upload_record.id,
            transactions=result.parsed_transactions
        )
        
        # Hydrate response with DB changes
        result.saved_transactions_count = saved_count
        return result
        
    except FileNotFoundError as e:
        logger.error(f"File processing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Temp file could not be found during parsing."
        )
    except Exception as e:
        logger.error(f"Unexpected error during parsing or database persistence: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while parsing or saving the file."
        )
    finally:
        # Cleanup: remove the temporary file safely
        if temp_file_path.exists():
            try:
                os.remove(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {temp_file_path}: {e}")

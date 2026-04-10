from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Upload(Base):
    __tablename__ = "uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now(), nullable=False)
    total_scanned = Column(Integer, default=0)
    valid_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    
    # 1-to-many relationship mapping
    transactions = relationship("Transaction", back_populates="upload", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    
    # Deterministic hash to strictly prevent duplication
    transaction_hash = Column(String, unique=True, index=True, nullable=False)
    
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(Date, nullable=True) # Standard PostgreSQL ISO Date
    month = Column(Integer, nullable=True)
    year = Column(Integer, nullable=True)
    day_of_week = Column(String, nullable=True)
    transaction_type = Column(String, nullable=False)
    category = Column(String, nullable=True)
    status = Column(String, nullable=False)
    
    date_raw = Column(String, nullable=False)
    raw_text = Column(String, nullable=False)
    source = Column(String, nullable=False)
    
    upload = relationship("Upload", back_populates="transactions")

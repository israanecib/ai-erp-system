"""
Expense model for financial tracking
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from datetime import datetime
import enum
from app.database import Base

class ExpenseCategory(str, enum.Enum):
    UTILITIES = "utilities"
    SALARIES = "salaries"
    RENT = "rent"
    SUPPLIES = "supplies"
    TRANSPORTATION = "transportation"
    MAINTENANCE = "maintenance"
    INSURANCE = "insurance"
    MARKETING = "marketing"
    OFFICE = "office"
    OTHER = "other"

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(200), nullable=False)
    category = Column(Enum(ExpenseCategory), default=ExpenseCategory.OTHER, nullable=False)
    amount = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receipt_reference = Column(String(100), nullable=True)
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Expense(id={self.id}, category={self.category}, amount={self.amount}, date={self.created_at})>"
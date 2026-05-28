"""
Invoice model for document tracking
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from datetime import datetime
import enum
from app.database import Base

class InvoiceStatus(str, enum.Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    currency = Column(String(3), default="EUR")
    due_date = Column(DateTime, nullable=True)
    notes = Column(String(500), nullable=True)
    is_recurring = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Invoice(id={self.id}, number={self.invoice_number}, customer_id={self.customer_id}, status={self.status})>"

    @property
    def balance_due(self):
        """Calculate remaining balance"""
        return self.total - self.amount_paid

    @property
    def is_overdue(self):
        """Check if invoice is overdue"""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and self.status != InvoiceStatus.PAID
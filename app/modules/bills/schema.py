from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal
from enum import Enum


class BillPaymentStatus(str, Enum):
    UNPAID = "UNPAID"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    OVERDUE = "OVERDUE"
    CANCELLED = "CANCELLED"


class BillItemCreate(BaseModel):
    item_name: str
    quantity: int
    unit_price: Decimal
    tax_percent: Decimal = 0


class BillCreate(BaseModel):
    vendor_code: str
    po_code: Optional[str] = None

    invoice_number: str
    invoice_date: date
    due_date: date

    notes: Optional[str] = None

    items: List[BillItemCreate]


class BillItemResponse(BaseModel):
    id: UUID

    item_name: str
    quantity: int

    unit_price: Decimal
    tax_percent: Decimal
    total: Decimal

    class Config:
        from_attributes = True


class BillResponse(BaseModel):
    id: UUID

    bill_code: str

    invoice_number: str

    payment_status: BillPaymentStatus

    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal

    invoice_date: date
    due_date: date

    notes: Optional[str]

    items: List[BillItemResponse]

    class Config:
        from_attributes = True


class BillUpdate(BaseModel):
    vendor_code: Optional[str] = None

    po_code: Optional[str] = None

    invoice_number: Optional[str] = None

    invoice_date: Optional[date] = None

    due_date: Optional[date] = None

    payment_status: Optional[BillPaymentStatus] = None

    notes: Optional[str] = None

    items: Optional[List[BillItemCreate]] = None
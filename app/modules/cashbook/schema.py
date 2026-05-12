from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date
from decimal import Decimal
from enum import Enum


class CashbookEntryType(str, Enum):
    IN = "IN"
    OUT = "OUT"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    BANK = "BANK"
    UPI = "UPI"
    CARD = "CARD"
    CHEQUE = "CHEQUE"


class CashbookEntryCreate(BaseModel):
    entry_type: CashbookEntryType

    amount: Decimal

    title: str

    notes: Optional[str] = None

    payment_method: PaymentMethod

    transaction_date: date

    attachment_url: Optional[str] = None


class CashbookEntryResponse(BaseModel):
    id: UUID

    entry_code: str

    entry_type: CashbookEntryType

    amount: Decimal

    title: str

    notes: Optional[str]

    payment_method: PaymentMethod

    transaction_date: date

    attachment_url: Optional[str]

    class Config:
        from_attributes = True

class CashbookEntryUpdate(BaseModel):
    entry_type: Optional[CashbookEntryType] = None

    amount: Optional[Decimal] = None

    title: Optional[str] = None

    notes: Optional[str] = None

    payment_method: Optional[PaymentMethod] = None

    transaction_date: Optional[date] = None

    attachment_url: Optional[str] = None
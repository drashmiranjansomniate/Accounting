from pydantic import BaseModel

from typing import List, Optional

from enum import Enum

from datetime import datetime


class QuotationStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class QuotationItemCreate(BaseModel):
    item_name: str
    quantity: int
    price: float
    tax_percent: float = 0


class QuotationCreate(BaseModel):
    customer_id: int
    notes: Optional[str] = None

    items: List[QuotationItemCreate]


class QuotationItemResponse(BaseModel):
    id: int
    item_name: str
    quantity: int
    price: float
    tax_percent: float
    total: float

    class Config:
        from_attributes = True


class QuotationResponse(BaseModel):
    id: int

    quotation_number: str

    status: QuotationStatus

    subtotal: float
    tax_amount: float
    total_amount: float

    notes: Optional[str]

    created_at: datetime

    items: List[QuotationItemResponse]

    class Config:
        from_attributes = True


class QuotationUpdate(BaseModel):
    status: Optional[QuotationStatus] = None

    notes: Optional[str] = None

    items: Optional[List[QuotationItemCreate]] = None
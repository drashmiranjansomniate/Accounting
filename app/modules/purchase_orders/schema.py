from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal
from enum import Enum


class PurchaseOrderStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PARTIALLY_RECEIVED = "PARTIALLY_RECEIVED"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"


class PurchaseOrderItemCreate(BaseModel):
    item_name: str
    quantity: int
    unit_price: Decimal
    tax_percent: Decimal = 0


class PurchaseOrderCreate(BaseModel):
    vendor_code: str
    order_date: date
    expected_delivery_date: Optional[date] = None
    notes: Optional[str] = None

    items: List[PurchaseOrderItemCreate]


class PurchaseOrderItemResponse(BaseModel):
    id: UUID
    item_name: str
    quantity: int
    unit_price: Decimal
    tax_percent: Decimal
    total: Decimal

    class Config:
        from_attributes = True


class PurchaseOrderResponse(BaseModel):
    id: UUID
    po_code: str
    status: PurchaseOrderStatus

    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal

    order_date: date
    expected_delivery_date: Optional[date]

    notes: Optional[str]

    items: List[PurchaseOrderItemResponse]

    class Config:
        from_attributes = True

class PurchaseOrderUpdate(BaseModel):
    vendor_code: str
    order_date: date
    expected_delivery_date: Optional[date] = None
    notes: Optional[str] = None

    items: List[PurchaseOrderItemCreate]
from pydantic import BaseModel

from typing import List, Optional

from enum import Enum

from datetime import datetime


class SalesOrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SalesOrderPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class SalesOrderItemCreate(BaseModel):
    item_name: str
    quantity: int
    price: float
    tax_percent: float = 0


class SalesOrderCreate(BaseModel):
    customer_id: int

    quotation_id: Optional[int] = None

    priority: Optional[SalesOrderPriority] = (
        SalesOrderPriority.MEDIUM
    )

    expected_delivery_date: Optional[datetime] = None

    notes: Optional[str] = None

    items: List[SalesOrderItemCreate]


class SalesOrderItemResponse(BaseModel):
    id: int

    item_name: str

    quantity: int

    price: float

    tax_percent: float

    total: float

    class Config:
        from_attributes = True


class SalesOrderResponse(BaseModel):
    id: int

    sales_order_number: str

    status: SalesOrderStatus

    priority: SalesOrderPriority

    subtotal: float

    tax_amount: float

    total_amount: float

    expected_delivery_date: Optional[datetime]

    notes: Optional[str]

    created_at: datetime

    items: List[SalesOrderItemResponse]

    class Config:
        from_attributes = True


class SalesOrderUpdate(BaseModel):
    status: Optional[SalesOrderStatus] = None

    priority: Optional[SalesOrderPriority] = None

    expected_delivery_date: Optional[datetime] = None

    notes: Optional[str] = None

    items: Optional[List[SalesOrderItemCreate]] = None
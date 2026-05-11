from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    ForeignKey,
    Enum,
    Numeric,
    Integer,
    Text
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

import uuid
import enum

from datetime import datetime


class PurchaseOrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    PARTIALLY_RECEIVED = "PARTIALLY_RECEIVED"
    RECEIVED = "RECEIVED"
    CANCELLED = "CANCELLED"


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    po_code = Column(
        String,
        unique=True,
        nullable=False
    )

    vendor_id = Column(
        UUID(as_uuid=True),
        ForeignKey("vendors.id"),
        nullable=False
    )

    order_date = Column(
        Date,
        nullable=False
    )

    expected_delivery_date = Column(Date)

    status = Column(
        Enum(PurchaseOrderStatus),
        default=PurchaseOrderStatus.PENDING,
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        default=0
    )

    tax_amount = Column(
        Numeric(10, 2),
        default=0
    )

    total_amount = Column(
        Numeric(10, 2),
        default=0
    )

    notes = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    vendor = relationship(
        "Vendor",
        backref="purchase_orders"
    )

    items = relationship(
        "PurchaseOrderItem",
        back_populates="purchase_order",
        cascade="all, delete"
    )


class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    purchase_order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("purchase_orders.id"),
        nullable=False
    )

    item_name = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    unit_price = Column(
        Numeric(10, 2),
        nullable=False
    )

    tax_percent = Column(
        Numeric(5, 2),
        default=0
    )

    total = Column(
        Numeric(10, 2),
        nullable=False
    )

    purchase_order = relationship(
        "PurchaseOrder",
        back_populates="items"
    )
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Enum
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

import enum

from app.core.database import Base


class SalesOrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SalesOrderPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class SalesOrder(Base):
    __tablename__ = "sales_orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id"),
        nullable=True
    )

    sales_order_number = Column(
        String,
        unique=True,
        nullable=False
    )

    status = Column(
        Enum(SalesOrderStatus),
        default=SalesOrderStatus.PENDING
    )

    priority = Column(
        Enum(SalesOrderPriority),
        default=SalesOrderPriority.MEDIUM
    )

    subtotal = Column(
        Float,
        default=0
    )

    tax_amount = Column(
        Float,
        default=0
    )

    total_amount = Column(
        Float,
        default=0
    )

    notes = Column(
        String,
        nullable=True
    )

    expected_delivery_date = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    customer = relationship(
        "Customer"
    )

    quotation = relationship(
        "Quotation"
    )

    items = relationship(
        "SalesOrderItem",
        back_populates="sales_order",
        cascade="all, delete"
    )


class SalesOrderItem(Base):
    __tablename__ = "sales_order_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    sales_order_id = Column(
        Integer,
        ForeignKey("sales_orders.id")
    )

    item_name = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    tax_percent = Column(
        Float,
        default=0
    )

    total = Column(
        Float,
        nullable=False
    )

    sales_order = relationship(
        "SalesOrder",
        back_populates="items"
    )
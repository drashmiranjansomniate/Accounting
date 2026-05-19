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

class SalesInvoiceItem(Base):
    __tablename__ = "sales_invoice_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    invoice_id = Column(
        Integer,
        ForeignKey("sales_invoices.id")
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
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

    invoice = relationship(
        "SalesInvoice",
        back_populates="items"
    )

    product = relationship("Product")
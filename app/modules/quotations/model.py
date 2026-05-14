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


class QuotationStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    quotation_number = Column(
        String,
        unique=True,
        nullable=False
    )

    status = Column(
        Enum(QuotationStatus),
        default=QuotationStatus.DRAFT
    )

    subtotal = Column(Float, default=0)

    tax_amount = Column(Float, default=0)

    total_amount = Column(Float, default=0)

    notes = Column(String, nullable=True)

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

    customer = relationship("Customer")

    items = relationship(
        "QuotationItem",
        back_populates="quotation",
        cascade="all, delete"
    )


class QuotationItem(Base):
    __tablename__ = "quotation_items"

    id = Column(Integer, primary_key=True, index=True)

    quotation_id = Column(
        Integer,
        ForeignKey("quotations.id")
    )

    item_name = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    tax_percent = Column(Float, default=0)

    total = Column(Float, nullable=False)

    quotation = relationship(
        "Quotation",
        back_populates="items"
    )
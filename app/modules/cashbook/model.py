from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    Enum,
    Numeric,
    Text,
    Integer,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

import uuid
import enum

from datetime import datetime


class CashbookEntryType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"


class PaymentMethod(str, enum.Enum):
    CASH = "CASH"
    BANK = "BANK"
    UPI = "UPI"
    CARD = "CARD"
    CHEQUE = "CHEQUE"


class CashbookEntry(Base):
    __tablename__ = "cashbook_entries"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    entry_code = Column(
        String,
        unique=True,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    entry_type = Column(
        Enum(CashbookEntryType),
        nullable=False
    )

    amount = Column(
        Numeric(18, 2),
        nullable=False
    )

    title = Column(
        String,
        nullable=False
    )

    notes = Column(Text)

    payment_method = Column(
        Enum(PaymentMethod),
        nullable=False
    )

    transaction_date = Column(
        Date,
        nullable=False
    )

    attachment_url = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
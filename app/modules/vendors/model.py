from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

import uuid
from datetime import datetime


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    vendor_code = Column(
        String,
        unique=True,
        nullable=False
    )

    vendor_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True
    )

    phone = Column(
        String,
        nullable=False
    )

    gst_number = Column(
        String,
        unique=True
    )

    address = Column(Text)

    city = Column(String)

    state = Column(String)

    pincode = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
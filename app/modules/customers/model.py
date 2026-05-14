from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from app.core.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    customer_name = Column(String, nullable=False)

    email = Column(String, nullable=True)

    phone = Column(String, nullable=True)

    gst_number = Column(String, nullable=True)

    billing_address = Column(String, nullable=True)

    shipping_address = Column(String, nullable=True)

    city = Column(String, nullable=True)

    state = Column(String, nullable=True)

    country = Column(String, nullable=True)

    pincode = Column(String, nullable=True)

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

    organization = relationship("Organization")

    user = relationship("User")
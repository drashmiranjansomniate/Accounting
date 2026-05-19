from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Boolean
)

from app.core.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

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

    name = Column(
        String,
        nullable=False
    )

    code = Column(
        String,
        nullable=False
    )

    address = Column(
        Text,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )
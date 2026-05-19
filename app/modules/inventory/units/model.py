from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.core.database import Base


class Unit(Base):
    __tablename__ = "units"

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

    short_name = Column(
        String,
        nullable=False
    )
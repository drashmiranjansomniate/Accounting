from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.core.database import Base


class OrganizationMember(Base):

    __tablename__ = "organization_members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    organization_id = Column(
        Integer,
        ForeignKey("organizations.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    role = Column(
        String,
        default="owner"
    )

    organization = relationship(
        "Organization"
    )

    user = relationship(
        "User"
    )
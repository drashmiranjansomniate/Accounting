from sqlalchemy.orm import Session

from app.modules.organization_members.model import (
    OrganizationMember
)


def get_user_organization_repo(
    db: Session,
    user_id: int
):

    return db.query(
        OrganizationMember
    ).filter(
        OrganizationMember.user_id == user_id
    ).first()
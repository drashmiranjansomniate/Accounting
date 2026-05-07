from sqlalchemy.orm import Session

from app.modules.vendors.schema import VendorCreate

from app.modules.vendors.repository import (
    create_vendor_repo,
    get_all_vendors_repo
)


def create_vendor_service(
    db: Session,
    vendor: VendorCreate
):
    # Future business logic goes here

    # Example:
    # validate duplicate GST
    # validate duplicate email
    # create audit logs
    # send notifications

    return create_vendor_repo(
        db=db,
        vendor=vendor
    )


def get_all_vendors_service(
    db: Session
):
    return get_all_vendors_repo(db)
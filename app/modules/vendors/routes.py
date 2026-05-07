from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db

from app.modules.vendors.schema import VendorCreate

from app.modules.vendors.service import (
    create_vendor_service,
    get_all_vendors_service
)

router = APIRouter(
    prefix="/vendors",
    tags=["Vendors"]
)


@router.post("/")
def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db)
):
    vendor_data = create_vendor_service(
        db=db,
        vendor=vendor
    )

    return {
        "message": "Vendor created successfully",
        "data": vendor_data
    }


@router.get("/")
def get_vendors(
    db: Session = Depends(get_db)
):
    vendors = get_all_vendors_service(db)

    return vendors
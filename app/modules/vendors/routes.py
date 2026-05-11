from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from fastapi import Query
from app.modules.vendors.schema import (
    VendorCreate,
    VendorUpdate
)

from app.modules.vendors.service import (
    create_vendor_service,
    get_all_vendors_service,
    get_vendor_by_code_service,
    update_vendor_service,
    delete_vendor_service
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
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    vendors = get_all_vendors_service(
        db=db,
        page=page,
        limit=limit
    )

    return {
        "page": page,
        "limit": limit,
        "data": vendors
    }


@router.get("/{vendor_code}")
def get_single_vendor(
    vendor_code: str,
    db: Session = Depends(get_db)
):
    vendor = get_vendor_by_code_service(
        db=db,
        vendor_code=vendor_code
    )

    return vendor


@router.patch("/{vendor_code}")
def update_vendor(
    vendor_code: str,
    vendor_update: VendorUpdate,
    db: Session = Depends(get_db)
):
    updated_vendor = update_vendor_service(
        db=db,
        vendor_code=vendor_code,
        vendor_update=vendor_update
    )

    return {
        "message": "Vendor updated successfully",
        "data": updated_vendor
    }


@router.delete("/{vendor_code}")
def delete_vendor(
    vendor_code: str,
    db: Session = Depends(get_db)
):
    return delete_vendor_service(
        db=db,
        vendor_code=vendor_code
    )
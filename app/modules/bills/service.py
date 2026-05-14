from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.modules.bills.schema import (
    BillCreate,
    BillUpdate
)

from app.modules.bills.repository import (
    create_bill_repo,
    get_all_bills_repo,
    get_total_bills_count_repo,
    get_bill_by_code_repo,
    delete_bill_repo,
    update_bill_repo
)

from app.modules.vendors.model import Vendor

from app.modules.purchase_orders.model import (
    PurchaseOrder
)


def create_bill_service(
    db: Session,
    bill: BillCreate,
    organization_id: int
):
    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_code == bill.vendor_code,
            Vendor.organization_id == organization_id
        )
        .first()
    )

    if not vendor:
        raise HTTPException(
            status_code=404,
            detail="Vendor not found"
        )

    if bill.po_code:

        purchase_order = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.po_code == bill.po_code,
                PurchaseOrder.organization_id == organization_id
            )
            .first()
        )

        if not purchase_order:
            raise HTTPException(
                status_code=404,
                detail="Purchase Order not found"
            )

    return create_bill_repo(
        db=db,
        bill=bill,
        organization_id=organization_id
    )


def get_all_bills_service(
    db: Session,
    page: int,
    limit: int,
    organization_id: int
):
    skip = (page - 1) * limit

    bills = get_all_bills_repo(
        db=db,
        skip=skip,
        limit=limit,
        organization_id=organization_id
    )

    total = get_total_bills_count_repo(
        db=db,
        organization_id=organization_id
    )

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "data": bills
    }


def get_bill_by_code_service(
    db: Session,
    bill_code: str,
    organization_id: int
):
    bill = get_bill_by_code_repo(
        db=db,
        bill_code=bill_code,
        organization_id=organization_id
    )

    if not bill:
        raise HTTPException(
            status_code=404,
            detail="Bill not found"
        )

    return bill


def delete_bill_service(
    db: Session,
    bill_code: str,
    organization_id: int
):
    bill = get_bill_by_code_repo(
        db=db,
        bill_code=bill_code,
        organization_id=organization_id
    )

    if not bill:
        raise HTTPException(
            status_code=404,
            detail="Bill not found"
        )

    delete_bill_repo(
        db=db,
        bill=bill
    )

    return {
        "message": "Bill deleted successfully"
    }


def update_bill_service(
    db: Session,
    bill_code: str,
    bill_update: BillUpdate,
    organization_id: int
):
    bill = get_bill_by_code_repo(
        db=db,
        bill_code=bill_code,
        organization_id=organization_id
    )

    if not bill:
        raise HTTPException(
            status_code=404,
            detail="Bill not found"
        )

    return update_bill_repo(
        db=db,
        bill=bill,
        bill_update=bill_update,
        organization_id=organization_id
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Query
from app.core.database import get_db

from app.modules.bills.schema import (
    BillCreate,
    BillUpdate
)

from app.modules.bills.service import (
    create_bill_service,
    get_all_bills_service,
    get_bill_by_code_service,
    delete_bill_service,
    update_bill_service
)

router = APIRouter(
    prefix="/bills",
    tags=["Bills"]
)


@router.post("/")
def create_bill(
    bill: BillCreate,
    db: Session = Depends(get_db)
):
    bill_data = create_bill_service(
        db=db,
        bill=bill
    )

    return {
        "message": "Bill created successfully",
        "data": bill_data
    }

@router.get("/")
def get_bills(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    bills = get_all_bills_service(
        db=db,
        page=page,
        limit=limit
    )

    return bills

@router.get("/{bill_code}")
def get_single_bill(
    bill_code: str,
    db: Session = Depends(get_db)
):
    bill = get_bill_by_code_service(
        db=db,
        bill_code=bill_code
    )

    return bill

@router.delete("/{bill_code}")
def delete_bill(
    bill_code: str,
    db: Session = Depends(get_db)
):
    return delete_bill_service(
        db=db,
        bill_code=bill_code
    )

@router.patch("/{bill_code}")
def update_bill(
    bill_code: str,
    bill_update: BillUpdate,
    db: Session = Depends(get_db)
):
    updated_bill = update_bill_service(
        db=db,
        bill_code=bill_code,
        bill_update=bill_update
    )

    return {
        "message": "Bill updated successfully",
        "data": updated_bill
    }
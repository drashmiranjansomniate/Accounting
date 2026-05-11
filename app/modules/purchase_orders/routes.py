from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from fastapi import Query
from app.modules.purchase_orders.schema import (
    PurchaseOrderCreate
)

from app.modules.purchase_orders.service import (
    create_purchase_order_service,
    get_all_purchase_orders_service
)

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"]
)

@router.get("/")
def get_purchase_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    purchase_orders = get_all_purchase_orders_service(
        db=db,
        page=page,
        limit=limit
    )

    return purchase_orders

@router.post("/")
def create_purchase_order(
    purchase_order: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    po = create_purchase_order_service(
        db=db,
        purchase_order=purchase_order
    )

    return {
        "message": "Purchase Order created successfully",
        "data": po
    }
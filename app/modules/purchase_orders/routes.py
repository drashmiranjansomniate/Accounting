from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.purchase_orders.schema import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate,
)

from app.modules.purchase_orders.service import (
    create_purchase_order_service,
    get_all_purchase_orders_service,
    delete_purchase_order_service,
    update_purchase_order_service,
)

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"]
)


@router.get("/")
def get_purchase_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):
    purchase_orders = get_all_purchase_orders_service(
        db=db,
        page=page,
        limit=limit,
        organization_id=organization_id
    )

    return purchase_orders


@router.post("/")
def create_purchase_order(
    purchase_order: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):
    po = create_purchase_order_service(
        db=db,
        purchase_order=purchase_order,
        organization_id=organization_id
    )

    return {
        "message": "Purchase Order created successfully",
        "data": po
    }


@router.delete("/{po_code}")
def delete_purchase_order(
    po_code: str,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):
    return delete_purchase_order_service(
        db=db,
        po_code=po_code,
        organization_id=organization_id
    )


@router.patch("/{po_code}")
def update_purchase_order(
    po_code: str,
    purchase_order_update: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):
    updated_po = update_purchase_order_service(
        db=db,
        po_code=po_code,
        purchase_order_update=purchase_order_update,
        organization_id=organization_id
    )

    return {
        "message": "Purchase Order updated successfully",
        "data": updated_po
    }
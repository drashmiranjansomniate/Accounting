from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_user,
    get_current_organization
)

from app.modules.sales_orders.schema import (
    SalesOrderCreate,
    SalesOrderUpdate
)

from app.modules.sales_orders.service import (
    create_sales_order_service,
    get_all_sales_orders_service,
    get_single_sales_order_service,
    update_sales_order_service,
    delete_sales_order_service
)

router = APIRouter(
    prefix="/sales-orders",
    tags=["Sales Orders"]
)


@router.post("/")
def create_sales_order(
    sales_order: SalesOrderCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    ),

    organization_id: int = Depends(
        get_current_organization
    )
):
    sales_order_data = create_sales_order_service(
        db=db,

        sales_order=sales_order,

        organization_id=organization_id,

        user_id=current_user.id
    )

    return {
        "message": "Sales Order created successfully",
        "data": sales_order_data
    }


@router.get("/")
def get_sales_orders(
    page: int = Query(1, ge=1),

    limit: int = Query(10, le=100),

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    sales_orders = get_all_sales_orders_service(
        db=db,

        page=page,

        limit=limit,

        organization_id=organization_id
    )

    return sales_orders


@router.get("/{sales_order_id}")
def get_single_sales_order(
    sales_order_id: int,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    sales_order = get_single_sales_order_service(
        db=db,

        sales_order_id=sales_order_id,

        organization_id=organization_id
    )

    return sales_order


@router.patch("/{sales_order_id}")
def update_sales_order(
    sales_order_id: int,

    sales_order_update: SalesOrderUpdate,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    updated_sales_order = update_sales_order_service(
        db=db,

        sales_order_id=sales_order_id,

        sales_order_update=sales_order_update,

        organization_id=organization_id
    )

    return {
        "message": "Sales Order updated successfully",
        "data": updated_sales_order
    }


@router.delete("/{sales_order_id}")
def delete_sales_order(
    sales_order_id: int,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    return delete_sales_order_service(
        db=db,

        sales_order_id=sales_order_id,

        organization_id=organization_id
    )
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

from app.modules.sales_invoices.schema import (
    SalesInvoiceCreate,
    SalesInvoiceUpdate
)

from app.modules.sales_invoices.service import (
    create_sales_invoice_service,
    get_all_sales_invoices_service,
    get_single_sales_invoice_service,
    update_sales_invoice_service,
    delete_sales_invoice_service
)

router = APIRouter(
    prefix="/sales-invoices",
    tags=["Sales Invoices"]
)


@router.post("/")
def create_sales_invoice(
    invoice: SalesInvoiceCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        get_current_user
    ),

    organization_id: int = Depends(
        get_current_organization
    )
):
    invoice_data = create_sales_invoice_service(
        db=db,

        invoice=invoice,

        organization_id=organization_id,

        user_id=current_user.id
    )

    return {
        "message": "Invoice created successfully",
        "data": invoice_data
    }


@router.get("/")
def get_sales_invoices(
    page: int = Query(1, ge=1),

    limit: int = Query(10, le=100),

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    invoices = get_all_sales_invoices_service(
        db=db,

        page=page,

        limit=limit,

        organization_id=organization_id
    )

    return invoices


@router.get("/{invoice_id}")
def get_single_sales_invoice(
    invoice_id: int,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    invoice = get_single_sales_invoice_service(
        db=db,

        invoice_id=invoice_id,

        organization_id=organization_id
    )

    return invoice


@router.patch("/{invoice_id}")
def update_sales_invoice(
    invoice_id: int,

    invoice_update: SalesInvoiceUpdate,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    updated_invoice = update_sales_invoice_service(
        db=db,

        invoice_id=invoice_id,

        invoice_update=invoice_update,

        organization_id=organization_id
    )

    return {
        "message": "Invoice updated successfully",
        "data": updated_invoice
    }


@router.delete("/{invoice_id}")
def delete_sales_invoice(
    invoice_id: int,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    return delete_sales_invoice_service(
        db=db,

        invoice_id=invoice_id,

        organization_id=organization_id
    )
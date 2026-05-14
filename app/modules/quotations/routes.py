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

from app.modules.quotations.schema import (
    QuotationCreate,
    QuotationUpdate
)

from app.modules.quotations.service import (
    create_quotation_service,
    get_all_quotations_service,
    get_single_quotation_service,
    update_quotation_service,
    delete_quotation_service
)

router = APIRouter(
    prefix="/quotations",
    tags=["Quotations"]
)


@router.post("/")
def create_quotation(
    quotation: QuotationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    organization_id: int = Depends(get_current_organization)
):
    quotation_data = create_quotation_service(
        db=db,
        quotation=quotation,
        organization_id=organization_id,
        user_id=current_user.id
    )

    return {
        "message": "Quotation created successfully",
        "data": quotation_data
    }


@router.get("/")
def get_quotations(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    quotations = get_all_quotations_service(
        db=db,
        page=page,
        limit=limit,
        organization_id=organization_id
    )

    return quotations


@router.get("/{quotation_id}")
def get_single_quotation(
    quotation_id: int,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    quotation = get_single_quotation_service(
        db=db,
        quotation_id=quotation_id,
        organization_id=organization_id
    )

    return quotation


@router.patch("/{quotation_id}")
def update_quotation(
    quotation_id: int,
    quotation_update: QuotationUpdate,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    updated_quotation = update_quotation_service(
        db=db,
        quotation_id=quotation_id,
        quotation_update=quotation_update,
        organization_id=organization_id
    )

    return {
        "message": "Quotation updated successfully",
        "data": updated_quotation
    }


@router.delete("/{quotation_id}")
def delete_quotation(
    quotation_id: int,

    db: Session = Depends(get_db),

    organization_id: int = Depends(
        get_current_organization
    )
):
    return delete_quotation_service(
        db=db,
        quotation_id=quotation_id,
        organization_id=organization_id
    )
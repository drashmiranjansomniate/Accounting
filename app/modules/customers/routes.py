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

from app.modules.customers.schema import (
    CustomerCreate,
    CustomerUpdate
)

from app.modules.customers.service import (
    create_customer_service,
    get_all_customers_service,
    get_single_customer_service,
    update_customer_service,
    delete_customer_service
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("/")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    organization_id: int = Depends(get_current_organization)
):
    return create_customer_service(
        db=db,
        customer=customer,
        organization_id=organization_id,
        user_id=current_user.id
    )


@router.get("/")
def get_all_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    organization_id: int = Depends(get_current_organization)
):
    return get_all_customers_service(
        db=db,
        organization_id=organization_id,
        page=page,
        limit=limit,
        search=search
    )


@router.get("/{customer_id}")
def get_single_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    organization_id: int = Depends(get_current_organization)
):
    return get_single_customer_service(
        db=db,
        customer_id=customer_id,
        organization_id=organization_id
    )


@router.patch("/{customer_id}")
def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    organization_id: int = Depends(get_current_organization)
):
    return update_customer_service(
        db=db,
        customer_id=customer_id,
        customer=customer,
        organization_id=organization_id
    )


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    organization_id: int = Depends(get_current_organization)
):
    return delete_customer_service(
        db=db,
        customer_id=customer_id,
        organization_id=organization_id
    )
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.inventory.products.schema import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

from app.modules.inventory.products.service import (
    create_product_service,
    get_all_products_service,
    get_product_by_id_service,
    update_product_service,
    delete_product_service
)

router = APIRouter(
    prefix="/products",
    tags=["Inventory Products"]
)


@router.post(
    "/",
    response_model=ProductResponse
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return create_product_service(
        db,
        product,
        organization_id
    )


@router.get(
    "/",
    response_model=List[ProductResponse]
)
def get_all_products(
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_all_products_service(
        db,
        organization_id
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_product_by_id_service(
        db,
        product_id,
        organization_id
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return update_product_service(
        db,
        product_id,
        product_data,
        organization_id
    )


@router.delete(
    "/{product_id}"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return delete_product_service(
        db,
        product_id,
        organization_id
    )
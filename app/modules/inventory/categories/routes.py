from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.inventory.categories.schema import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)

from app.modules.inventory.categories.service import (
    create_category_service,
    get_all_categories_service,
    get_category_by_id_service,
    update_category_service,
    delete_category_service
)

router = APIRouter(
    prefix="/categories",
    tags=["Inventory Categories"]
)


@router.post(
    "/",
    response_model=CategoryResponse
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return create_category_service(
        db,
        category,
        organization_id
    )


@router.get(
    "/",
    response_model=List[CategoryResponse]
)
def get_all_categories(
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_all_categories_service(
        db,
        organization_id
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse
)
def get_category_by_id(
    category_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_category_by_id_service(
        db,
        category_id,
        organization_id
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return update_category_service(
        db,
        category_id,
        category_data,
        organization_id
    )


@router.delete(
    "/{category_id}"
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return delete_category_service(
        db,
        category_id,
        organization_id
    )
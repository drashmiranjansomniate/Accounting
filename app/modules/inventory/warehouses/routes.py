from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.inventory.warehouses.schema import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseResponse
)

from app.modules.inventory.warehouses.service import (
    create_warehouse_service,
    get_all_warehouses_service,
    get_warehouse_by_id_service,
    update_warehouse_service,
    delete_warehouse_service
)

router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)


@router.post(
    "/",
    response_model=WarehouseResponse
)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return create_warehouse_service(
        db,
        warehouse,
        organization_id
    )


@router.get(
    "/",
    response_model=List[WarehouseResponse]
)
def get_all_warehouses(
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_all_warehouses_service(
        db,
        organization_id
    )


@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def get_warehouse_by_id(
    warehouse_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_warehouse_by_id_service(
        db,
        warehouse_id,
        organization_id
    )


@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def update_warehouse(
    warehouse_id: int,
    warehouse_data: WarehouseUpdate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return update_warehouse_service(
        db,
        warehouse_id,
        warehouse_data,
        organization_id
    )


@router.delete(
    "/{warehouse_id}"
)
def delete_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return delete_warehouse_service(
        db,
        warehouse_id,
        organization_id
    )
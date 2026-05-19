from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.inventory.units.schema import (
    UnitCreate,
    UnitUpdate,
    UnitResponse
)

from app.modules.inventory.units.service import (
    create_unit_service,
    get_all_units_service,
    get_unit_by_id_service,
    update_unit_service,
    delete_unit_service
)

router = APIRouter(
    prefix="/units",
    tags=["Inventory Units"]
)


@router.post(
    "/",
    response_model=UnitResponse
)
def create_unit(
    unit: UnitCreate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return create_unit_service(
        db,
        unit,
        organization_id
    )


@router.get(
    "/",
    response_model=List[UnitResponse]
)
def get_all_units(
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_all_units_service(
        db,
        organization_id
    )


@router.get(
    "/{unit_id}",
    response_model=UnitResponse
)
def get_unit_by_id(
    unit_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_unit_by_id_service(
        db,
        unit_id,
        organization_id
    )


@router.put(
    "/{unit_id}",
    response_model=UnitResponse
)
def update_unit(
    unit_id: int,
    unit_data: UnitUpdate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return update_unit_service(
        db,
        unit_id,
        unit_data,
        organization_id
    )


@router.delete(
    "/{unit_id}"
)
def delete_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return delete_unit_service(
        db,
        unit_id,
        organization_id
    )
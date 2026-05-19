from sqlalchemy.orm import Session

from app.modules.inventory.units.model import Unit
from app.modules.inventory.units.schema import (
    UnitUpdate
)


def create_unit_repo(
    db: Session,
    unit: Unit
):
    db.add(unit)

    db.commit()

    db.refresh(unit)

    return unit


def get_all_units_repo(
    db: Session,
    organization_id: int
):

    return db.query(Unit).filter(
        Unit.organization_id == organization_id
    ).all()


def get_unit_by_id_repo(
    db: Session,
    unit_id: int,
    organization_id: int
):

    return db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.organization_id == organization_id
    ).first()


def update_unit_repo(
    db: Session,
    unit_obj: Unit,
    unit_data: UnitUpdate
):

    if unit_data.name is not None:
        unit_obj.name = unit_data.name

    if unit_data.short_name is not None:
        unit_obj.short_name = unit_data.short_name

    db.commit()

    db.refresh(unit_obj)

    return unit_obj


def delete_unit_repo(
    db: Session,
    unit_obj: Unit
):

    db.delete(unit_obj)

    db.commit()
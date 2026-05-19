from sqlalchemy.orm import Session

from app.modules.inventory.warehouses.model import (
    Warehouse
)

from app.modules.inventory.warehouses.schema import (
    WarehouseUpdate
)


def create_warehouse_repo(
    db: Session,
    warehouse: Warehouse
):

    db.add(warehouse)

    db.commit()

    db.refresh(warehouse)

    return warehouse


def get_all_warehouses_repo(
    db: Session,
    organization_id: int
):

    return db.query(Warehouse).filter(
        Warehouse.organization_id == organization_id
    ).all()


def get_warehouse_by_id_repo(
    db: Session,
    warehouse_id: int,
    organization_id: int
):

    return db.query(Warehouse).filter(
        Warehouse.id == warehouse_id,
        Warehouse.organization_id == organization_id
    ).first()


def get_warehouse_by_code_repo(
    db: Session,
    code: str,
    organization_id: int
):

    return db.query(Warehouse).filter(
        Warehouse.code == code,
        Warehouse.organization_id == organization_id
    ).first()


def update_warehouse_repo(
    db: Session,
    warehouse_obj: Warehouse,
    warehouse_data: WarehouseUpdate
):

    update_data = warehouse_data.dict(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(warehouse_obj, key, value)

    db.commit()

    db.refresh(warehouse_obj)

    return warehouse_obj


def delete_warehouse_repo(
    db: Session,
    warehouse_obj: Warehouse
):

    db.delete(warehouse_obj)

    db.commit()
from sqlalchemy.orm import Session

from app.modules.inventory.categories.model import Category
from app.modules.inventory.categories.schema import (
    CategoryCreate,
    CategoryUpdate
)


def create_category_repo(
    db: Session,
    category: Category
):
    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_all_categories_repo(
    db: Session,
    organization_id: int
):
    return db.query(Category).filter(
        Category.organization_id == organization_id
    ).all()


def get_category_by_id_repo(
    db: Session,
    category_id: int,
    organization_id: int
):
    return db.query(Category).filter(
        Category.id == category_id,
        Category.organization_id == organization_id
    ).first()


def update_category_repo(
    db: Session,
    category_obj: Category,
    category_data: CategoryUpdate
):

    if category_data.name is not None:
        category_obj.name = category_data.name

    if category_data.description is not None:
        category_obj.description = category_data.description

    db.commit()
    db.refresh(category_obj)

    return category_obj


def delete_category_repo(
    db: Session,
    category_obj: Category
):
    db.delete(category_obj)

    db.commit()
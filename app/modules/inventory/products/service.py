from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.inventory.products.model import Product

from app.modules.inventory.products.schema import (
    ProductCreate,
    ProductUpdate
)

from app.modules.inventory.products.repository import (
    create_product_repo,
    get_all_products_repo,
    get_product_by_id_repo,
    get_product_by_sku_repo,
    update_product_repo,
    delete_product_repo
)

from app.modules.inventory.categories.model import Category
from app.modules.inventory.units.model import Unit


def create_product_service(
    db: Session,
    product: ProductCreate,
    organization_id: int
):

    existing_sku = get_product_by_sku_repo(
        db,
        product.sku,
        organization_id
    )

    if existing_sku:

        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    category = db.query(Category).filter(
        Category.id == product.category_id,
        Category.organization_id == organization_id
    ).first()

    if not category:

        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    unit = db.query(Unit).filter(
        Unit.id == product.unit_id,
        Unit.organization_id == organization_id
    ).first()

    if not unit:

        raise HTTPException(
            status_code=404,
            detail="Unit not found"
        )

    new_product = Product(
        organization_id=organization_id,

        name=product.name,
        sku=product.sku,

        category_id=product.category_id,
        unit_id=product.unit_id,

        barcode=product.barcode,

        purchase_price=product.purchase_price,
        selling_price=product.selling_price,

        gst_percent=product.gst_percent,

        opening_stock=product.opening_stock,
        current_stock=product.current_stock,
        minimum_stock=product.minimum_stock,

        description=product.description
    )

    return create_product_repo(
        db,
        new_product
    )


def get_all_products_service(
    db: Session,
    organization_id: int
):

    return get_all_products_repo(
        db,
        organization_id
    )


def get_product_by_id_service(
    db: Session,
    product_id: int,
    organization_id: int
):

    product = get_product_by_id_repo(
        db,
        product_id,
        organization_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


def update_product_service(
    db: Session,
    product_id: int,
    product_data: ProductUpdate,
    organization_id: int
):

    product = get_product_by_id_repo(
        db,
        product_id,
        organization_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product_data.category_id:

        category = db.query(Category).filter(
            Category.id == product_data.category_id,
            Category.organization_id == organization_id
        ).first()

        if not category:

            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    if product_data.unit_id:

        unit = db.query(Unit).filter(
            Unit.id == product_data.unit_id,
            Unit.organization_id == organization_id
        ).first()

        if not unit:

            raise HTTPException(
                status_code=404,
                detail="Unit not found"
            )

    return update_product_repo(
        db,
        product,
        product_data
    )


def delete_product_service(
    db: Session,
    product_id: int,
    organization_id: int
):

    product = get_product_by_id_repo(
        db,
        product_id,
        organization_id
    )

    if not product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    delete_product_repo(
        db,
        product
    )

    return {
        "message": "Product deleted successfully"
    }
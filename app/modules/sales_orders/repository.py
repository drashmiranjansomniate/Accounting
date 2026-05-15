from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.modules.sales_orders.model import (
    SalesOrder,
    SalesOrderItem
)

from app.modules.sales_orders.schema import (
    SalesOrderCreate,
    SalesOrderUpdate
)


def get_all_sales_orders_repo(
    db: Session,
    skip: int,
    limit: int,
    organization_id: int
):
    return (
        db.query(SalesOrder)
        .options(
            joinedload(SalesOrder.items),
            joinedload(SalesOrder.customer),
            joinedload(SalesOrder.quotation)
        )
        .filter(
            SalesOrder.organization_id == organization_id
        )
        .order_by(
            SalesOrder.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_total_sales_orders_count_repo(
    db: Session,
    organization_id: int
):
    return (
        db.query(SalesOrder)
        .filter(
            SalesOrder.organization_id == organization_id
        )
        .count()
    )


def get_sales_order_by_id_repo(
    db: Session,
    sales_order_id: int,
    organization_id: int
):
    return (
        db.query(SalesOrder)
        .options(
            joinedload(SalesOrder.items),
            joinedload(SalesOrder.customer),
            joinedload(SalesOrder.quotation)
        )
        .filter(
            SalesOrder.id == sales_order_id,
            SalesOrder.organization_id == organization_id
        )
        .first()
    )


def create_sales_order_repo(
    db: Session,
    sales_order: SalesOrderCreate,
    organization_id: int,
    user_id: int
):
    last_order = (
        db.query(SalesOrder)
        .order_by(SalesOrder.id.desc())
        .first()
    )

    current_year = 2026

    if last_order:
        new_number = (
            f"SO-{current_year}-{last_order.id + 1:04d}"
        )
    else:
        new_number = (
            f"SO-{current_year}-0001"
        )

    subtotal = 0
    tax_amount = 0

    for item in sales_order.items:

        item_total = (
            item.quantity * item.price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / 100

        subtotal += item_total

        tax_amount += item_tax

    total_amount = subtotal + tax_amount

    new_sales_order = SalesOrder(
        organization_id=organization_id,

        customer_id=sales_order.customer_id,

        quotation_id=sales_order.quotation_id,

        sales_order_number=new_number,

        priority=sales_order.priority,

        expected_delivery_date=(
            sales_order.expected_delivery_date
        ),

        subtotal=subtotal,

        tax_amount=tax_amount,

        total_amount=total_amount,

        notes=sales_order.notes,

        created_by=user_id
    )

    db.add(new_sales_order)

    db.commit()

    db.refresh(new_sales_order)

    for item in sales_order.items:

        item_total = (
            item.quantity * item.price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / 100

        final_total = item_total + item_tax

        new_item = SalesOrderItem(
            sales_order_id=new_sales_order.id,

            item_name=item.item_name,

            quantity=item.quantity,

            price=item.price,

            tax_percent=item.tax_percent,

            total=final_total
        )

        db.add(new_item)

    db.commit()

    db.refresh(new_sales_order)

    return new_sales_order


def update_sales_order_repo(
    db: Session,
    sales_order,
    sales_order_update: SalesOrderUpdate
):
    if sales_order_update.status:
        sales_order.status = (
            sales_order_update.status
        )

    if sales_order_update.priority:
        sales_order.priority = (
            sales_order_update.priority
        )

    if sales_order_update.expected_delivery_date:
        sales_order.expected_delivery_date = (
            sales_order_update.expected_delivery_date
        )

    if sales_order_update.notes:
        sales_order.notes = (
            sales_order_update.notes
        )

    if sales_order_update.items:

        subtotal = 0
        tax_amount = 0

        db.query(SalesOrderItem).filter(
            SalesOrderItem.sales_order_id == sales_order.id
        ).delete()

        for item in sales_order_update.items:

            item_total = (
                item.quantity * item.price
            )

            item_tax = (
                item_total * item.tax_percent
            ) / 100

            subtotal += item_total

            tax_amount += item_tax

            final_total = item_total + item_tax

            new_item = SalesOrderItem(
                sales_order_id=sales_order.id,

                item_name=item.item_name,

                quantity=item.quantity,

                price=item.price,

                tax_percent=item.tax_percent,

                total=final_total
            )

            db.add(new_item)

        sales_order.subtotal = subtotal

        sales_order.tax_amount = tax_amount

        sales_order.total_amount = (
            subtotal + tax_amount
        )

    db.commit()

    db.refresh(sales_order)

    return sales_order


def delete_sales_order_repo(
    db: Session,
    sales_order
):
    db.delete(sales_order)

    db.commit()

    return True
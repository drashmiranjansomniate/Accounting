from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from decimal import Decimal

from app.modules.purchase_orders.model import (
    PurchaseOrder,
    PurchaseOrderItem
)

from app.modules.purchase_orders.schema import (
    PurchaseOrderCreate,
    PurchaseOrderUpdate
)

from app.modules.vendors.model import Vendor


def get_all_purchase_orders_repo(
    db: Session,
    skip: int,
    limit: int,
    organization_id: int
):
    return (
        db.query(PurchaseOrder)
        .options(
            joinedload(PurchaseOrder.items),
            joinedload(PurchaseOrder.vendor)
        )
        .filter(
            PurchaseOrder.organization_id == organization_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_purchase_order_by_code_repo(
    db: Session,
    po_code: str,
    organization_id: int
):
    return (
        db.query(PurchaseOrder)
        .options(
            joinedload(PurchaseOrder.items),
            joinedload(PurchaseOrder.vendor)
        )
        .filter(
            PurchaseOrder.po_code == po_code,
            PurchaseOrder.organization_id == organization_id
        )
        .first()
    )


def delete_purchase_order_repo(
    db: Session,
    purchase_order
):
    db.delete(purchase_order)
    db.commit()

    return True


def get_total_purchase_orders_count_repo(
    db: Session,
    organization_id: int
):
    return (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.organization_id == organization_id
        )
        .count()
    )


def create_purchase_order_repo(
    db: Session,
    purchase_order: PurchaseOrderCreate,
    organization_id: int
):
    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_code == purchase_order.vendor_code,
            Vendor.organization_id == organization_id
        )
        .first()
    )

    last_po = (
        db.query(PurchaseOrder)
        .order_by(PurchaseOrder.created_at.desc())
        .first()
    )

    if last_po:

        last_number = int(
            last_po.po_code.replace("PO-", "")
        )

        new_po_code = f"PO-{last_number + 1:04d}"

    else:
        new_po_code = "PO-0001"

    subtotal = Decimal("0")
    total_tax = Decimal("0")

    for item in purchase_order.items:

        item_total = (
            item.quantity * item.unit_price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / Decimal("100")

        subtotal += item_total
        total_tax += item_tax

    grand_total = subtotal + total_tax

    new_po = PurchaseOrder(
        po_code=new_po_code,
        vendor_id=vendor.id,
        organization_id=organization_id,
        order_date=purchase_order.order_date,
        expected_delivery_date=purchase_order.expected_delivery_date,
        subtotal=subtotal,
        tax_amount=total_tax,
        total_amount=grand_total,
        notes=purchase_order.notes
    )

    db.add(new_po)
    db.commit()
    db.refresh(new_po)

    for item in purchase_order.items:

        item_total = (
            item.quantity * item.unit_price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / Decimal("100")

        final_total = item_total + item_tax

        new_item = PurchaseOrderItem(
            purchase_order_id=new_po.id,
            item_name=item.item_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            tax_percent=item.tax_percent,
            total=final_total
        )

        db.add(new_item)

    db.commit()
    db.refresh(new_po)

    return new_po


def update_purchase_order_repo(
    db: Session,
    purchase_order,
    purchase_order_update: PurchaseOrderUpdate,
    organization_id: int
):
    vendor = (
        db.query(Vendor)
        .filter(
            Vendor.vendor_code == purchase_order_update.vendor_code,
            Vendor.organization_id == organization_id
        )
        .first()
    )

    subtotal = Decimal("0")
    total_tax = Decimal("0")

    for item in purchase_order_update.items:

        item_total = (
            item.quantity * item.unit_price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / Decimal("100")

        subtotal += item_total
        total_tax += item_tax

    grand_total = subtotal + total_tax

    purchase_order.vendor_id = vendor.id
    purchase_order.order_date = purchase_order_update.order_date

    purchase_order.expected_delivery_date = (
        purchase_order_update.expected_delivery_date
    )

    purchase_order.notes = purchase_order_update.notes

    purchase_order.subtotal = subtotal
    purchase_order.tax_amount = total_tax
    purchase_order.total_amount = grand_total

    db.query(PurchaseOrderItem).filter(
        PurchaseOrderItem.purchase_order_id == purchase_order.id
    ).delete()

    for item in purchase_order_update.items:

        item_total = (
            item.quantity * item.unit_price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / Decimal("100")

        final_total = item_total + item_tax

        new_item = PurchaseOrderItem(
            purchase_order_id=purchase_order.id,
            item_name=item.item_name,
            quantity=item.quantity,
            unit_price=item.unit_price,
            tax_percent=item.tax_percent,
            total=final_total
        )

        db.add(new_item)

    db.commit()
    db.refresh(purchase_order)

    return purchase_order
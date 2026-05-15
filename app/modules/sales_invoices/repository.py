from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.modules.sales_invoices.model import (
    SalesInvoice,
    SalesInvoiceItem
)

from app.modules.sales_invoices.schema import (
    SalesInvoiceCreate,
    SalesInvoiceUpdate
)


def get_all_sales_invoices_repo(
    db: Session,
    skip: int,
    limit: int,
    organization_id: int
):
    return (
        db.query(SalesInvoice)
        .options(
            joinedload(SalesInvoice.items),
            joinedload(SalesInvoice.customer),
            joinedload(SalesInvoice.sales_order)
        )
        .filter(
            SalesInvoice.organization_id == organization_id
        )
        .order_by(
            SalesInvoice.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_total_sales_invoices_count_repo(
    db: Session,
    organization_id: int
):
    return (
        db.query(SalesInvoice)
        .filter(
            SalesInvoice.organization_id == organization_id
        )
        .count()
    )


def get_sales_invoice_by_id_repo(
    db: Session,
    invoice_id: int,
    organization_id: int
):
    return (
        db.query(SalesInvoice)
        .options(
            joinedload(SalesInvoice.items),
            joinedload(SalesInvoice.customer),
            joinedload(SalesInvoice.sales_order)
        )
        .filter(
            SalesInvoice.id == invoice_id,
            SalesInvoice.organization_id == organization_id
        )
        .first()
    )


def create_sales_invoice_repo(
    db: Session,
    invoice: SalesInvoiceCreate,
    organization_id: int,
    user_id: int
):
    last_invoice = (
        db.query(SalesInvoice)
        .order_by(SalesInvoice.id.desc())
        .first()
    )

    current_year = 2026

    if last_invoice:
        invoice_number = (
            f"INV-{current_year}-{last_invoice.id + 1:04d}"
        )
    else:
        invoice_number = (
            f"INV-{current_year}-0001"
        )

    subtotal = 0
    tax_amount = 0

    for item in invoice.items:

        item_total = (
            item.quantity * item.price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / 100

        subtotal += item_total

        tax_amount += item_tax

    total_amount = subtotal + tax_amount

    new_invoice = SalesInvoice(
        organization_id=organization_id,

        customer_id=invoice.customer_id,

        sales_order_id=invoice.sales_order_id,

        invoice_number=invoice_number,

        subtotal=subtotal,

        tax_amount=tax_amount,

        total_amount=total_amount,

        paid_amount=0,

        due_amount=total_amount,

        notes=invoice.notes,

        due_date=invoice.due_date,

        created_by=user_id
    )

    db.add(new_invoice)

    db.commit()

    db.refresh(new_invoice)

    for item in invoice.items:

        item_total = (
            item.quantity * item.price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / 100

        final_total = (
            item_total + item_tax
        )

        new_item = SalesInvoiceItem(
            invoice_id=new_invoice.id,

            item_name=item.item_name,

            quantity=item.quantity,

            price=item.price,

            tax_percent=item.tax_percent,

            total=final_total
        )

        db.add(new_item)

    db.commit()

    db.refresh(new_invoice)

    return new_invoice


def update_sales_invoice_repo(
    db: Session,
    invoice,
    invoice_update: SalesInvoiceUpdate
):
    if invoice_update.status:
        invoice.status = (
            invoice_update.status
        )

    if invoice_update.notes:
        invoice.notes = (
            invoice_update.notes
        )

    if invoice_update.due_date:
        invoice.due_date = (
            invoice_update.due_date
        )

    if invoice_update.paid_amount is not None:

        invoice.paid_amount = (
            invoice_update.paid_amount
        )

        invoice.due_amount = (
            invoice.total_amount
            - invoice.paid_amount
        )

        if invoice.paid_amount == 0:
            invoice.status = "SENT"

        elif (
            invoice.paid_amount
            < invoice.total_amount
        ):
            invoice.status = (
                "PARTIALLY_PAID"
            )

        elif (
            invoice.paid_amount
            >= invoice.total_amount
        ):
            invoice.status = "PAID"

    db.commit()

    db.refresh(invoice)

    return invoice


def delete_sales_invoice_repo(
    db: Session,
    invoice
):
    db.delete(invoice)

    db.commit()

    return True
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.modules.quotations.model import (
    Quotation,
    QuotationItem
)

from app.modules.quotations.schema import (
    QuotationCreate,
    QuotationUpdate
)


def get_all_quotations_repo(
    db: Session,
    skip: int,
    limit: int,
    organization_id: int
):
    return (
        db.query(Quotation)
        .options(
            joinedload(Quotation.items),
            joinedload(Quotation.customer)
        )
        .filter(
            Quotation.organization_id == organization_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_total_quotations_count_repo(
    db: Session,
    organization_id: int
):
    return (
        db.query(Quotation)
        .filter(
            Quotation.organization_id == organization_id
        )
        .count()
    )


def get_quotation_by_id_repo(
    db: Session,
    quotation_id: int,
    organization_id: int
):
    return (
        db.query(Quotation)
        .options(
            joinedload(Quotation.items),
            joinedload(Quotation.customer)
        )
        .filter(
            Quotation.id == quotation_id,
            Quotation.organization_id == organization_id
        )
        .first()
    )


def create_quotation_repo(
    db: Session,
    quotation: QuotationCreate,
    organization_id: int,
    user_id: int
):
    last_quotation = (
        db.query(Quotation)
        .order_by(Quotation.id.desc())
        .first()
    )

    if last_quotation:
        new_number = (
            f"QT-{last_quotation.id + 1:04d}"
        )
    else:
        new_number = "QT-0001"

    subtotal = 0
    tax_amount = 0

    for item in quotation.items:

        item_total = (
            item.quantity * item.price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / 100

        subtotal += item_total
        tax_amount += item_tax

    total_amount = subtotal + tax_amount

    new_quotation = Quotation(
        quotation_number=new_number,
        organization_id=organization_id,
        customer_id=quotation.customer_id,

        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,

        notes=quotation.notes,

        created_by=user_id
    )

    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)

    for item in quotation.items:

        item_total = (
            item.quantity * item.price
        )

        item_tax = (
            item_total * item.tax_percent
        ) / 100

        final_total = item_total + item_tax

        new_item = QuotationItem(
            quotation_id=new_quotation.id,

            item_name=item.item_name,
            quantity=item.quantity,
            price=item.price,
            tax_percent=item.tax_percent,

            total=final_total
        )

        db.add(new_item)

    db.commit()
    db.refresh(new_quotation)

    return new_quotation


def update_quotation_repo(
    db: Session,
    quotation,
    quotation_update: QuotationUpdate
):
    if quotation_update.status:
        quotation.status = quotation_update.status

    if quotation_update.notes:
        quotation.notes = quotation_update.notes

    if quotation_update.items:

        subtotal = 0
        tax_amount = 0

        db.query(QuotationItem).filter(
            QuotationItem.quotation_id == quotation.id
        ).delete()

        for item in quotation_update.items:

            item_total = (
                item.quantity * item.price
            )

            item_tax = (
                item_total * item.tax_percent
            ) / 100

            subtotal += item_total
            tax_amount += item_tax

            final_total = item_total + item_tax

            new_item = QuotationItem(
                quotation_id=quotation.id,

                item_name=item.item_name,
                quantity=item.quantity,
                price=item.price,
                tax_percent=item.tax_percent,

                total=final_total
            )

            db.add(new_item)

        quotation.subtotal = subtotal
        quotation.tax_amount = tax_amount
        quotation.total_amount = (
            subtotal + tax_amount
        )

    db.commit()
    db.refresh(quotation)

    return quotation


def delete_quotation_repo(
    db: Session,
    quotation
):
    db.delete(quotation)
    db.commit()

    return True
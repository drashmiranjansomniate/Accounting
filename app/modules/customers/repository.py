from sqlalchemy.orm import Session

from sqlalchemy import or_

from app.modules.customers.model import Customer

from app.modules.customers.schema import (
    CustomerCreate,
    CustomerUpdate
)


def create_customer_repo(
    db: Session,
    customer: CustomerCreate,
    organization_id: int,
    user_id: int
):
    new_customer = Customer(
        **customer.model_dump(),
        organization_id=organization_id,
        created_by=user_id
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def get_all_customers_repo(
    db: Session,
    organization_id: int,
    page: int,
    limit: int,
    search: str = None
):
    query = db.query(Customer).filter(
        Customer.organization_id == organization_id
    )

    if search:
        query = query.filter(
            or_(
                Customer.customer_name.ilike(f"%{search}%"),
                Customer.email.ilike(f"%{search}%"),
                Customer.phone.ilike(f"%{search}%"),
                Customer.gst_number.ilike(f"%{search}%")
            )
        )

    skip = (page - 1) * limit

    customers = query.offset(skip).limit(limit).all()

    total = query.count()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": customers
    }


def get_single_customer_repo(
    db: Session,
    customer_id: int,
    organization_id: int
):
    return db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.organization_id == organization_id
    ).first()


def update_customer_repo(
    db: Session,
    existing_customer: Customer,
    customer: CustomerUpdate
):
    update_data = customer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_customer, key, value)

    db.commit()
    db.refresh(existing_customer)

    return existing_customer


def delete_customer_repo(
    db: Session,
    customer: Customer
):
    db.delete(customer)

    db.commit()
from sqlalchemy.orm import Session

from app.modules.inventory.stock_transactions.model import (
    StockTransaction
)


def create_stock_transaction_repo(
    db: Session,
    stock_transaction: StockTransaction
):

    db.add(stock_transaction)

    db.commit()

    db.refresh(stock_transaction)

    return stock_transaction


def get_all_stock_transactions_repo(
    db: Session,
    organization_id: int
):

    return db.query(StockTransaction).filter(
        StockTransaction.organization_id == organization_id
    ).all()


def get_product_stock_transactions_repo(
    db: Session,
    product_id: int,
    organization_id: int
):

    return db.query(StockTransaction).filter(
        StockTransaction.product_id == product_id,
        StockTransaction.organization_id == organization_id
    ).all()
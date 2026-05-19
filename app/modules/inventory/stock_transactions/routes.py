from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from app.core.dependencies import (
    get_current_organization
)

from app.modules.inventory.stock_transactions.schema import (
    StockTransactionCreate,
    StockTransactionResponse
)

from app.modules.inventory.stock_transactions.service import (
    create_stock_transaction_service,
    get_all_stock_transactions_service,
    get_product_stock_transactions_service
)

router = APIRouter(
    prefix="/stock-transactions",
    tags=["Stock Transactions"]
)


@router.post(
    "/",
    response_model=StockTransactionResponse
)
def create_stock_transaction(
    transaction: StockTransactionCreate,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return create_stock_transaction_service(
        db,
        transaction,
        organization_id
    )


@router.get(
    "/",
    response_model=List[StockTransactionResponse]
)
def get_all_stock_transactions(
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_all_stock_transactions_service(
        db,
        organization_id
    )


@router.get(
    "/product/{product_id}",
    response_model=List[StockTransactionResponse]
)
def get_product_stock_transactions(
    product_id: int,
    db: Session = Depends(get_db),
    organization_id: int = Depends(get_current_organization)
):

    return get_product_stock_transactions_service(
        db,
        product_id,
        organization_id
    )
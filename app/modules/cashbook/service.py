from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.modules.cashbook.schema import (
    CashbookEntryCreate,
    CashbookEntryUpdate
)

from app.modules.cashbook.repository import (
    create_cashbook_entry_repo,
    get_all_cashbook_entries_repo,
    get_total_cashbook_entries_count_repo,
    get_cashbook_entry_by_code_repo,
    delete_cashbook_entry_repo,
    update_cashbook_entry_repo
)


def create_cashbook_entry_service(
    db: Session,
    entry: CashbookEntryCreate
):
    if entry.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )

    return create_cashbook_entry_repo(
        db=db,
        entry=entry
    )


def get_all_cashbook_entries_service(
    db: Session,
    page: int,
    limit: int
):
    skip = (page - 1) * limit

    entries = get_all_cashbook_entries_repo(
        db=db,
        skip=skip,
        limit=limit
    )

    total = get_total_cashbook_entries_count_repo(db)

    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "data": entries
    }


def get_cashbook_entry_by_code_service(
    db: Session,
    entry_code: str
):
    entry = get_cashbook_entry_by_code_repo(
        db=db,
        entry_code=entry_code
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Cashbook entry not found"
        )

    return entry


def delete_cashbook_entry_service(
    db: Session,
    entry_code: str
):
    entry = get_cashbook_entry_by_code_repo(
        db=db,
        entry_code=entry_code
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Cashbook entry not found"
        )

    delete_cashbook_entry_repo(
        db=db,
        entry=entry
    )

    return {
        "message": "Cashbook entry deleted successfully"
    }


def update_cashbook_entry_service(
    db: Session,
    entry_code: str,
    entry_update: CashbookEntryUpdate
):
    entry = get_cashbook_entry_by_code_repo(
        db=db,
        entry_code=entry_code
    )

    if not entry:
        raise HTTPException(
            status_code=404,
            detail="Cashbook entry not found"
        )

    if entry_update.amount is not None:

        if entry_update.amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )

    return update_cashbook_entry_repo(
        db=db,
        entry=entry,
        entry_update=entry_update
    )
from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.core.dependencies import (
    get_current_user
)

from app.modules.cashbook.schema import (
    CashbookEntryCreate,
    CashbookEntryUpdate
)

from app.modules.cashbook.service import (
    create_cashbook_entry_service,
    get_all_cashbook_entries_service,
    get_cashbook_entry_by_code_service,
    delete_cashbook_entry_service,
    update_cashbook_entry_service
)

router = APIRouter(
    prefix="/cashbook",
    tags=["Cashbook"]
)


@router.post("/")
def create_cashbook_entry(
    entry: CashbookEntryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    entry_data = create_cashbook_entry_service(
        db=db,
        entry=entry,
        user_id=current_user.id
    )

    return {
        "message": "Cashbook entry created successfully",
        "data": entry_data
    }


@router.get("/")
def get_cashbook_entries(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    entries = get_all_cashbook_entries_service(
        db=db,
        page=page,
        limit=limit,
        user_id=current_user.id
    )

    return entries


@router.get("/{entry_code}")
def get_single_cashbook_entry(
    entry_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    entry = get_cashbook_entry_by_code_service(
        db=db,
        entry_code=entry_code,
        user_id=current_user.id
    )

    return entry


@router.delete("/{entry_code}")
def delete_cashbook_entry(
    entry_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return delete_cashbook_entry_service(
        db=db,
        entry_code=entry_code,
        user_id=current_user.id
    )


@router.patch("/{entry_code}")
def update_cashbook_entry(
    entry_code: str,
    entry_update: CashbookEntryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_entry = update_cashbook_entry_service(
        db=db,
        entry_code=entry_code,
        entry_update=entry_update,
        user_id=current_user.id
    )

    return {
        "message": "Cashbook entry updated successfully",
        "data": updated_entry
    }
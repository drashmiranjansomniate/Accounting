from pydantic import BaseModel
from typing import Optional


class WarehouseBase(BaseModel):

    name: str
    code: str

    address: Optional[str] = None


class WarehouseCreate(
    WarehouseBase
):
    pass


class WarehouseUpdate(BaseModel):

    name: Optional[str] = None
    code: Optional[str] = None

    address: Optional[str] = None

    is_active: Optional[bool] = None


class WarehouseResponse(
    WarehouseBase
):

    id: int

    organization_id: int

    is_active: bool

    class Config:
        from_attributes = True
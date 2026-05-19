from pydantic import BaseModel
from typing import Optional


class UnitBase(BaseModel):
    name: str
    short_name: str


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    name: Optional[str] = None
    short_name: Optional[str] = None


class UnitResponse(UnitBase):
    id: int
    organization_id: int

    class Config:
        from_attributes = True
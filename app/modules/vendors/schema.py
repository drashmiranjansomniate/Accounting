from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from enum import Enum

class VendorStatus(str, Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    OVERDUE = "OVERDUE"

class VendorCreate(BaseModel):
    vendor_name: str
    email: Optional[EmailStr] = None
    phone: str
    gst_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    status: VendorStatus = VendorStatus.UNPAID


class VendorResponse(VendorCreate):
    id: UUID
    vendor_code: str

    class Config:
        from_attributes = True
from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class VendorCreate(BaseModel):
    vendor_name: str
    email: Optional[EmailStr] = None
    phone: str
    gst_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None


class VendorResponse(VendorCreate):
    id: UUID
    vendor_code: str

    class Config:
        from_attributes = True
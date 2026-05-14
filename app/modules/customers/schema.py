from pydantic import BaseModel, EmailStr

from typing import Optional

from datetime import datetime


class CustomerCreate(BaseModel):
    customer_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    gst_number: Optional[str] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    gst_number: Optional[str] = None
    billing_address: Optional[str] = None
    shipping_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    organization_id: int
    customer_name: str
    email: Optional[str]
    phone: Optional[str]
    gst_number: Optional[str]
    billing_address: Optional[str]
    shipping_address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    pincode: Optional[str]
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True
from sqlalchemy.orm import Session

from app.modules.vendors.model import Vendor
from app.modules.vendors.schema import VendorCreate


def create_vendor_repo(
    db: Session,
    vendor: VendorCreate
):
    last_vendor = (
        db.query(Vendor)
        .order_by(Vendor.created_at.desc())
        .first()
    )

    if last_vendor:
        last_number = int(last_vendor.vendor_code.replace("V", ""))
        new_vendor_code = f"V{last_number + 1}"
    else:
        new_vendor_code = "V1"

    new_vendor = Vendor(
        vendor_code=new_vendor_code,
        vendor_name=vendor.vendor_name,
        email=vendor.email,
        phone=vendor.phone,
        gst_number=vendor.gst_number,
        address=vendor.address,
        city=vendor.city,
        state=vendor.state,
        pincode=vendor.pincode
    )

    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)

    return new_vendor


def get_all_vendors_repo(
    db: Session
):
    return db.query(Vendor).all()
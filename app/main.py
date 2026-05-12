from fastapi import FastAPI

from app.core.database import Base
from app.core.database import engine

from app.modules.vendors.model import Vendor
from app.modules.vendors.routes import router as vendor_router

from app.modules.purchase_orders.model import (
    PurchaseOrder,
    PurchaseOrderItem
)
from app.modules.bills.model import (
    Bill,
    BillItem
)
from app.modules.bills.routes import (
    router as bill_router
)
from app.modules.purchase_orders.routes import (
    router as purchase_order_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Accounting SaaS API",
    version="1.0.0"
)

app.include_router(vendor_router)
app.include_router(purchase_order_router)
app.include_router(bill_router)

@app.get("/")
def home():
    return {
        "message": "Accounting Backend Running Successfully"
    }
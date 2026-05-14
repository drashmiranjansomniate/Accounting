from fastapi import FastAPI


from app.modules.vendors.model import Vendor

from app.modules.vendors.routes import router as vendor_router
from app.modules.auth.routes import router as auth_router

from app.modules.purchase_orders.model import (
    PurchaseOrder,
    PurchaseOrderItem
)
from app.modules.bills.model import (
    Bill,
    BillItem
)
from app.modules.cashbook.model import (
    CashbookEntry
)
# Routers links
from app.modules.bills.routes import (
    router as bill_router
)
from app.modules.purchase_orders.routes import (
    router as purchase_order_router
)
from app.modules.cashbook.routes import (
    router as cashbook_router
)
from app.modules.customers.routes import(
    router as customers_router
)
from app.modules.quotations.routes import(
    router as quotations_router
)

from app.modules.users.model import User
from app.modules.organizations.model import Organization
from app.modules.organization_members.model import OrganizationMember

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Accounting SaaS API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(vendor_router)
app.include_router(purchase_order_router)
app.include_router(bill_router)
app.include_router(cashbook_router)
app.include_router(auth_router)
app.include_router(customers_router)
app.include_router(quotations_router)


@app.get("/")
def home():
    return {
        "message": "Accounting Backend Running Successfully"
    }
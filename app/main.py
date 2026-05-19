

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.modules.vendors.model import Vendor

from app.modules.vendors.routes import router as vendor_router
from app.modules.auth.routes import router as auth_router

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
from app.modules.sales_orders.routes import(
    router as sales_router
)
from app.modules.sales_invoices.routes import(
    router as sales_invoice_router
)
from app.modules.inventory.categories.routes import(
    router as categories_router
)
from app.modules.inventory.units.routes import (
    router as unit_router
)
from app.modules.inventory.products.routes import (
    router as products_router
)
from app.modules.inventory.stock_transactions.routes import (
    router as stock_transaction_router
)
from app.modules.inventory.warehouses.routes import(
    router as warehouse_router
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles


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

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploads folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(vendor_router)
app.include_router(purchase_order_router)
app.include_router(bill_router)
app.include_router(cashbook_router)
app.include_router(customers_router)
app.include_router(quotations_router)
app.include_router(sales_router)
app.include_router(sales_invoice_router)
app.include_router(categories_router)
app.include_router(unit_router)
app.include_router(products_router)
app.include_router(stock_transaction_router)
app.include_router(warehouse_router)


@app.get("/")
def home():
    return {
        "message": "Accounting Backend Running Successfully"
    }
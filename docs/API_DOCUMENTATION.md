# Accounting SaaS API Documentation

This document describes the API implemented in this project from the route, schema, and service files.

Base URL for local development:

```text
http://localhost:8000
```

Interactive FastAPI docs, when the app is running:

```text
http://localhost:8000/docs
http://localhost:8000/redoc
```

## Authentication

Most endpoints require a Bearer token returned from `POST /auth/login`.

```http
Authorization: Bearer <access_token>
```

Public endpoints:

- `GET /`
- `POST /auth/send-otp`
- `POST /auth/verify-otp`
- `POST /auth/register`
- `POST /auth/login`

Protected endpoints:

- All other endpoints.

Common FastAPI error response:

```json
{
  "detail": "Error message"
}
```

Validation errors return FastAPI's standard `422 Unprocessable Entity` response.

## Common Query Parameters

Paginated endpoints use:

| Name | Type | Default | Rule |
| --- | --- | --- | --- |
| `page` | integer | `1` | Must be `>= 1` |
| `limit` | integer | `10` | Must be `<= 100` |

Common paginated response shape:

```json
{
  "page": 1,
  "limit": 10,
  "total": 25,
  "total_pages": 3,
  "has_next": true,
  "has_previous": false,
  "data": []
}
```

## Root

### Health Check

| Method | Endpoint | Auth | Body |
| --- | --- | --- | --- |
| `GET` | `/` | No | None |

Response:

```json
{
  "message": "Accounting Backend Running Successfully"
}
```

## Authentication APIs

### Send OTP

| Method | Endpoint | Auth |
| --- | --- | --- |
| `POST` | `/auth/send-otp` | No |

Body:

```json
{
  "email": "owner@example.com"
}
```

Success response:

```json
{
  "message": "OTP sent successfully"
}
```

Possible errors:

- `400`: `Email already registered`

### Verify OTP

| Method | Endpoint | Auth |
| --- | --- | --- |
| `POST` | `/auth/verify-otp` | No |

Body:

```json
{
  "email": "owner@example.com",
  "otp": "123456"
}
```

Success response:

```json
{
  "message": "OTP verified successfully"
}
```

Possible errors:

- `400`: `Invalid or expired OTP`

### Register

| Method | Endpoint | Auth | Content Type |
| --- | --- | --- | --- |
| `POST` | `/auth/register` | No | `multipart/form-data` |

Form fields:

| Field | Type | Required |
| --- | --- | --- |
| `organization_type` | string | Yes |
| `organization_name` | string | Yes |
| `email` | email | Yes |
| `password` | string | Yes |
| `gst_number` | string | No |
| `phone` | string | No |
| `address` | string | No |
| `photo` | file | No, jpg/jpeg/png only |

Success response:

```json
{
  "message": "Account created successfully"
}
```

Possible errors:

- `400`: `Invalid image format`
- `400`: `Email not verified`
- `400`: `Email already registered`

### Login

| Method | Endpoint | Auth |
| --- | --- | --- |
| `POST` | `/auth/login` | No |

Body:

```json
{
  "email": "owner@example.com",
  "password": "password123"
}
```

Success response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "owner@example.com"
  },
  "organization": {
    "id": 1,
    "organization_name": "Acme Pvt Ltd",
    "organization_type": "COMPANY",
    "gst_number": "22AAAAA0000A1Z5",
    "phone": "9999999999",
    "address": "Office address",
    "photo": "uploads/organizations/owner_example.com.png",
    "created_at": "2026-05-18T10:00:00"
  }
}
```

Possible errors:

- `400`: `Invalid email or password`
- `404`: `Organization membership not found`
- `404`: `Organization not found`

### Current User

| Method | Endpoint | Auth | Body |
| --- | --- | --- | --- |
| `GET` | `/auth/me` | Yes | None |

Response:

```json
{
  "id": 1,
  "email": "owner@example.com"
}
```

### My Organization

| Method | Endpoint | Auth | Body |
| --- | --- | --- | --- |
| `GET` | `/auth/my-organization` | Yes | None |

Intended response:

```json
{
  "organization_id": 1,
  "role": "OWNER"
}
```

Implementation note: `get_current_organization` currently returns an integer organization id, but this route reads it as an object with `organization_id` and `role`. This endpoint may need a small code fix before it works as documented.

### Profile

| Method | Endpoint | Auth | Body |
| --- | --- | --- | --- |
| `GET` | `/auth/profile` | Yes | None |

Response:

```json
{
  "user": {
    "id": 1,
    "email": "owner@example.com"
  },
  "organization": {
    "id": 1,
    "organization_name": "Acme Pvt Ltd",
    "organization_type": "COMPANY",
    "gst_number": "22AAAAA0000A1Z5",
    "phone": "9999999999",
    "address": "Office address",
    "photo": "uploads/organizations/owner_example.com.png",
    "created_at": "2026-05-18T10:00:00"
  },
  "membership": {
    "role": "OWNER"
  }
}
```

## Vendors APIs

Vendor status values: `PAID`, `UNPAID`, `OVERDUE`.

Vendor create body:

```json
{
  "vendor_name": "ABC Traders",
  "email": "vendor@example.com",
  "phone": "9999999999",
  "gst_number": "22AAAAA0000A1Z5",
  "address": "Vendor address",
  "city": "Delhi",
  "state": "Delhi",
  "pincode": "110001",
  "status": "UNPAID"
}
```

Vendor response shape:

```json
{
  "id": "uuid",
  "vendor_code": "VEN-0001",
  "vendor_name": "ABC Traders",
  "email": "vendor@example.com",
  "phone": "9999999999",
  "gst_number": "22AAAAA0000A1Z5",
  "address": "Vendor address",
  "city": "Delhi",
  "state": "Delhi",
  "pincode": "110001",
  "status": "UNPAID"
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/vendors/` | Yes | Vendor create body | `{ "message": "Vendor created successfully", "data": Vendor }` |
| `GET` | `/vendors/?page=1&limit=10` | Yes | None | `{ "page": 1, "limit": 10, "data": [Vendor] }` |
| `GET` | `/vendors/{vendor_code}` | No token dependency in route | None | `Vendor` |
| `PATCH` | `/vendors/{vendor_code}` | No token dependency in route | Any vendor create field optional | `{ "message": "Vendor updated successfully", "data": Vendor }` |
| `DELETE` | `/vendors/{vendor_code}` | No token dependency in route | None | `{ "message": "Vendor deleted successfully" }` |

Possible errors:

- `400`: `Email already exists`
- `404`: `Vendor not found`

## Customers APIs

Customer create body:

```json
{
  "customer_name": "Rahul Sharma",
  "email": "customer@example.com",
  "phone": "9999999999",
  "gst_number": "22AAAAA0000A1Z5",
  "billing_address": "Billing address",
  "shipping_address": "Shipping address",
  "city": "Delhi",
  "state": "Delhi",
  "country": "India",
  "pincode": "110001"
}
```

Customer response shape:

```json
{
  "id": 1,
  "organization_id": 1,
  "customer_name": "Rahul Sharma",
  "email": "customer@example.com",
  "phone": "9999999999",
  "gst_number": "22AAAAA0000A1Z5",
  "billing_address": "Billing address",
  "shipping_address": "Shipping address",
  "city": "Delhi",
  "state": "Delhi",
  "country": "India",
  "pincode": "110001",
  "created_by": 1,
  "created_at": "2026-05-18T10:00:00"
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/customers/` | Yes | Customer create body | `Customer` |
| `GET` | `/customers/?page=1&limit=10&search=rahul` | Yes | None | Service list response |
| `GET` | `/customers/{customer_id}` | Yes | None | `Customer` |
| `PATCH` | `/customers/{customer_id}` | Yes | Any customer create field optional | `Customer` |
| `DELETE` | `/customers/{customer_id}` | Yes | None | `{ "message": "Customer deleted successfully" }` |

Possible errors:

- `400`: `Customer email already exists`
- `400`: `GST number already exists`
- `404`: `Customer not found`

## Cashbook APIs

Entry types: `IN`, `OUT`.

Payment methods: `CASH`, `BANK`, `UPI`, `CARD`, `CHEQUE`.

Cashbook create body:

```json
{
  "entry_type": "IN",
  "amount": 1500.0,
  "title": "Cash sale",
  "notes": "Daily sale collection",
  "payment_method": "CASH",
  "transaction_date": "2026-05-18",
  "attachment_url": "uploads/cashbook/receipt.pdf"
}
```

Cashbook response shape:

```json
{
  "id": "uuid",
  "entry_code": "CB-0001",
  "entry_type": "IN",
  "amount": 1500.0,
  "title": "Cash sale",
  "notes": "Daily sale collection",
  "payment_method": "CASH",
  "transaction_date": "2026-05-18",
  "attachment_url": "uploads/cashbook/receipt.pdf"
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/cashbook/` | Yes | Cashbook create body | `{ "message": "Cashbook entry created successfully", "data": CashbookEntry }` |
| `GET` | `/cashbook/?page=1&limit=10` | Yes | None | Paginated response with `data: [CashbookEntry]` |
| `GET` | `/cashbook/{entry_code}` | Yes | None | `CashbookEntry` |
| `PATCH` | `/cashbook/{entry_code}` | Yes | Any cashbook create field optional | `{ "message": "Cashbook entry updated successfully", "data": CashbookEntry }` |
| `DELETE` | `/cashbook/{entry_code}` | Yes | None | `{ "message": "Cashbook entry deleted successfully" }` |

Possible errors:

- `400`: `Amount must be greater than 0`
- `404`: `Cashbook entry not found`

## Purchase Orders APIs

Purchase order status values: `PENDING`, `APPROVED`, `PARTIALLY_RECEIVED`, `RECEIVED`, `CANCELLED`.

Purchase order create/update body:

```json
{
  "vendor_code": "VEN-0001",
  "order_date": "2026-05-18",
  "expected_delivery_date": "2026-05-25",
  "notes": "Purchase note",
  "items": [
    {
      "item_name": "Laptop",
      "quantity": 2,
      "unit_price": 50000.0,
      "tax_percent": 18.0
    }
  ]
}
```

Purchase order response shape:

```json
{
  "id": "uuid",
  "po_code": "PO-0001",
  "status": "PENDING",
  "subtotal": 100000.0,
  "tax_amount": 18000.0,
  "total_amount": 118000.0,
  "order_date": "2026-05-18",
  "expected_delivery_date": "2026-05-25",
  "notes": "Purchase note",
  "items": [
    {
      "id": "uuid",
      "item_name": "Laptop",
      "quantity": 2,
      "unit_price": 50000.0,
      "tax_percent": 18.0,
      "total": 118000.0
    }
  ]
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `GET` | `/purchase-orders/?page=1&limit=10` | Yes | None | Paginated response with `data: [PurchaseOrder]` |
| `POST` | `/purchase-orders/` | Yes | Purchase order body | `{ "message": "Purchase Order created successfully", "data": PurchaseOrder }` |
| `PATCH` | `/purchase-orders/{po_code}` | Yes | Purchase order body | `{ "message": "Purchase Order updated successfully", "data": PurchaseOrder }` |
| `DELETE` | `/purchase-orders/{po_code}` | Yes | None | `{ "message": "Purchase Order deleted successfully" }` |

Possible errors:

- `404`: `Vendor not found`
- `404`: `Purchase Order not found`

## Bills APIs

Bill payment status values: `UNPAID`, `PARTIALLY_PAID`, `PAID`, `OVERDUE`, `CANCELLED`.

Bill create body:

```json
{
  "vendor_code": "VEN-0001",
  "po_code": "PO-0001",
  "invoice_number": "INV-001",
  "invoice_date": "2026-05-18",
  "due_date": "2026-06-18",
  "notes": "Bill note",
  "items": [
    {
      "item_name": "Laptop",
      "quantity": 2,
      "unit_price": 50000.0,
      "tax_percent": 18.0
    }
  ]
}
```

Bill update body: all create fields are optional, plus:

```json
{
  "payment_status": "PAID"
}
```

Bill response shape:

```json
{
  "id": "uuid",
  "bill_code": "BILL-0001",
  "invoice_number": "INV-001",
  "payment_status": "UNPAID",
  "subtotal": 100000.0,
  "tax_amount": 18000.0,
  "total_amount": 118000.0,
  "invoice_date": "2026-05-18",
  "due_date": "2026-06-18",
  "notes": "Bill note",
  "items": [
    {
      "id": "uuid",
      "item_name": "Laptop",
      "quantity": 2,
      "unit_price": 50000.0,
      "tax_percent": 18.0,
      "total": 118000.0
    }
  ]
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/bills/` | Yes | Bill create body | `{ "message": "Bill created successfully", "data": Bill }` |
| `GET` | `/bills/?page=1&limit=10` | Yes | None | Paginated response with `data: [Bill]` |
| `GET` | `/bills/{bill_code}` | Yes | None | `Bill` |
| `PATCH` | `/bills/{bill_code}` | Yes | Bill update body | `{ "message": "Bill updated successfully", "data": Bill }` |
| `DELETE` | `/bills/{bill_code}` | Yes | None | `{ "message": "Bill deleted successfully" }` |

Possible errors:

- `404`: `Vendor not found`
- `404`: `Purchase Order not found`
- `404`: `Bill not found`

## Quotations APIs

Quotation status values: `DRAFT`, `SENT`, `ACCEPTED`, `REJECTED`, `EXPIRED`.

Quotation create body:

```json
{
  "customer_id": 1,
  "notes": "Quotation note",
  "items": [
    {
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0
    }
  ]
}
```

Quotation update body:

```json
{
  "status": "SENT",
  "notes": "Updated note",
  "items": [
    {
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0
    }
  ]
}
```

Quotation response shape:

```json
{
  "id": 1,
  "quotation_number": "QT-0001",
  "status": "DRAFT",
  "subtotal": 50000.0,
  "tax_amount": 9000.0,
  "total_amount": 59000.0,
  "notes": "Quotation note",
  "created_at": "2026-05-18T10:00:00",
  "items": [
    {
      "id": 1,
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0,
      "total": 59000.0
    }
  ]
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/quotations/` | Yes | Quotation create body | `{ "message": "Quotation created successfully", "data": Quotation }` |
| `GET` | `/quotations/?page=1&limit=10` | Yes | None | Paginated response with `data: [Quotation]` |
| `GET` | `/quotations/{quotation_id}` | Yes | None | `Quotation` |
| `PATCH` | `/quotations/{quotation_id}` | Yes | Quotation update body | `{ "message": "Quotation updated successfully", "data": Quotation }` |
| `DELETE` | `/quotations/{quotation_id}` | Yes | None | `{ "message": "Quotation deleted successfully" }` |

Possible errors:

- `404`: `Customer not found`
- `404`: `Quotation not found`
- `400`: `Cannot delete quotation. Sales Order already exists.`

## Sales Orders APIs

Sales order status values: `PENDING`, `CONFIRMED`, `PROCESSING`, `COMPLETED`, `CANCELLED`.

Sales order priority values: `LOW`, `MEDIUM`, `HIGH`, `URGENT`.

Sales order create body:

```json
{
  "customer_id": 1,
  "quotation_id": 1,
  "priority": "MEDIUM",
  "expected_delivery_date": "2026-05-25T10:00:00",
  "notes": "Sales order note",
  "items": [
    {
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0
    }
  ]
}
```

Sales order update body:

```json
{
  "status": "CONFIRMED",
  "priority": "HIGH",
  "expected_delivery_date": "2026-05-25T10:00:00",
  "notes": "Updated note",
  "items": [
    {
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0
    }
  ]
}
```

Sales order response shape:

```json
{
  "id": 1,
  "sales_order_number": "SO-0001",
  "status": "PENDING",
  "priority": "MEDIUM",
  "subtotal": 50000.0,
  "tax_amount": 9000.0,
  "total_amount": 59000.0,
  "expected_delivery_date": "2026-05-25T10:00:00",
  "notes": "Sales order note",
  "created_at": "2026-05-18T10:00:00",
  "items": [
    {
      "id": 1,
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0,
      "total": 59000.0
    }
  ]
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/sales-orders/` | Yes | Sales order create body | `{ "message": "Sales Order created successfully", "data": SalesOrder }` |
| `GET` | `/sales-orders/?page=1&limit=10` | Yes | None | Paginated response with `data: [SalesOrder]` |
| `GET` | `/sales-orders/{sales_order_id}` | Yes | None | `SalesOrder` |
| `PATCH` | `/sales-orders/{sales_order_id}` | Yes | Sales order update body | `{ "message": "Sales Order updated successfully", "data": SalesOrder }` |
| `DELETE` | `/sales-orders/{sales_order_id}` | Yes | None | `{ "message": "Sales Order deleted successfully" }` |

Possible errors:

- `404`: `Customer not found`
- `404`: `Quotation not found`
- `404`: `Sales Order not found`
- `400`: `Cannot delete Sales Order. Invoice already exists.`

## Sales Invoices APIs

Invoice status values: `DRAFT`, `SENT`, `PARTIALLY_PAID`, `PAID`, `OVERDUE`, `CANCELLED`.

Sales invoice create body:

```json
{
  "customer_id": 1,
  "sales_order_id": 1,
  "due_date": "2026-06-18T10:00:00",
  "notes": "Invoice note",
  "items": [
    {
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0
    }
  ]
}
```

Sales invoice update body:

```json
{
  "status": "PARTIALLY_PAID",
  "paid_amount": 25000.0,
  "due_date": "2026-06-18T10:00:00",
  "notes": "Payment received"
}
```

Sales invoice response shape:

```json
{
  "id": 1,
  "invoice_number": "INV-0001",
  "status": "DRAFT",
  "subtotal": 50000.0,
  "tax_amount": 9000.0,
  "total_amount": 59000.0,
  "paid_amount": 0.0,
  "due_amount": 59000.0,
  "notes": "Invoice note",
  "due_date": "2026-06-18T10:00:00",
  "created_at": "2026-05-18T10:00:00",
  "items": [
    {
      "id": 1,
      "item_name": "Website Development",
      "quantity": 1,
      "price": 50000.0,
      "tax_percent": 18.0,
      "total": 59000.0
    }
  ]
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/sales-invoices/` | Yes | Sales invoice create body | `{ "message": "Invoice created successfully", "data": SalesInvoice }` |
| `GET` | `/sales-invoices/?page=1&limit=10` | Yes | None | Paginated response with `data: [SalesInvoice]` |
| `GET` | `/sales-invoices/{invoice_id}` | Yes | None | `SalesInvoice` |
| `PATCH` | `/sales-invoices/{invoice_id}` | Yes | Sales invoice update body | `{ "message": "Invoice updated successfully", "data": SalesInvoice }` |
| `DELETE` | `/sales-invoices/{invoice_id}` | Yes | None | `{ "message": "Invoice deleted successfully" }` |

Possible errors:

- `404`: `Customer not found`
- `404`: `Sales Order not found`
- `404`: `Invoice not found`

## Inventory Categories APIs

Category create body:

```json
{
  "name": "Electronics",
  "description": "Electronic items"
}
```

Category response shape:

```json
{
  "id": 1,
  "organization_id": 1,
  "name": "Electronics",
  "description": "Electronic items"
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/categories/` | Yes | Category create body | `Category` |
| `GET` | `/categories/` | Yes | None | `[Category]` |
| `GET` | `/categories/{category_id}` | Yes | None | `Category` |
| `PUT` | `/categories/{category_id}` | Yes | `{ "name": "Electronics", "description": "Updated" }` with all fields optional | `Category` |
| `DELETE` | `/categories/{category_id}` | Yes | None | `{ "message": "Category deleted successfully" }` |

Possible errors:

- `400`: `Category already exists`
- `404`: `Category not found`

## Inventory Units APIs

Unit create body:

```json
{
  "name": "Piece",
  "short_name": "pcs"
}
```

Unit response shape:

```json
{
  "id": 1,
  "organization_id": 1,
  "name": "Piece",
  "short_name": "pcs"
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/units/` | Yes | Unit create body | `Unit` |
| `GET` | `/units/` | Yes | None | `[Unit]` |
| `GET` | `/units/{unit_id}` | Yes | None | `Unit` |
| `PUT` | `/units/{unit_id}` | Yes | `{ "name": "Box", "short_name": "box" }` with all fields optional | `Unit` |
| `DELETE` | `/units/{unit_id}` | Yes | None | `{ "message": "Unit deleted successfully" }` |

Possible errors:

- `400`: `Unit already exists`
- `404`: `Unit not found`

## Inventory Products APIs

Product create body:

```json
{
  "name": "Laptop",
  "sku": "LAP-001",
  "category_id": 1,
  "unit_id": 1,
  "barcode": "1234567890123",
  "purchase_price": 50000.0,
  "selling_price": 60000.0,
  "gst_percent": 18.0,
  "opening_stock": 10.0,
  "current_stock": 10.0,
  "minimum_stock": 2.0,
  "description": "Business laptop"
}
```

Product response shape:

```json
{
  "id": 1,
  "organization_id": 1,
  "name": "Laptop",
  "sku": "LAP-001",
  "category_id": 1,
  "unit_id": 1,
  "barcode": "1234567890123",
  "purchase_price": 50000.0,
  "selling_price": 60000.0,
  "gst_percent": 18.0,
  "opening_stock": 10.0,
  "current_stock": 10.0,
  "minimum_stock": 2.0,
  "description": "Business laptop",
  "is_active": true
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/products/` | Yes | Product create body | `Product` |
| `GET` | `/products/` | Yes | None | `[Product]` |
| `GET` | `/products/{product_id}` | Yes | None | `Product` |
| `PUT` | `/products/{product_id}` | Yes | Any product create field optional, plus `is_active` | `Product` |
| `DELETE` | `/products/{product_id}` | Yes | None | `{ "message": "Product deleted successfully" }` |

Possible errors:

- `400`: `SKU already exists`
- `404`: `Product not found`
- `404`: `Category not found`
- `404`: `Unit not found`

## Warehouses APIs

Warehouse create body:

```json
{
  "name": "Main Warehouse",
  "code": "WH-001",
  "address": "Warehouse address"
}
```

Warehouse response shape:

```json
{
  "id": 1,
  "organization_id": 1,
  "name": "Main Warehouse",
  "code": "WH-001",
  "address": "Warehouse address",
  "is_active": true
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/warehouses/` | Yes | Warehouse create body | `Warehouse` |
| `GET` | `/warehouses/` | Yes | None | `[Warehouse]` |
| `GET` | `/warehouses/{warehouse_id}` | Yes | None | `Warehouse` |
| `PUT` | `/warehouses/{warehouse_id}` | Yes | Any warehouse create field optional, plus `is_active` | `Warehouse` |
| `DELETE` | `/warehouses/{warehouse_id}` | Yes | None | `{ "message": "Warehouse deleted successfully" }` |

Possible errors:

- `400`: `Warehouse code already exists`
- `404`: `Warehouse not found`

## Stock Transactions APIs

Accepted transaction types:

- Increases stock: `OPENING`, `PURCHASE`, `RETURN`, `ADJUSTMENT_IN`
- Decreases stock: `SALE`, `DAMAGE`, `ADJUSTMENT_OUT`

Stock transaction create body:

```json
{
  "product_id": 1,
  "transaction_type": "PURCHASE",
  "quantity": 5.0,
  "reference_type": "PURCHASE_ORDER",
  "reference_id": 1,
  "remarks": "Stock received"
}
```

Stock transaction response shape:

```json
{
  "id": 1,
  "organization_id": 1,
  "product_id": 1,
  "transaction_type": "PURCHASE",
  "quantity": 5.0,
  "reference_type": "PURCHASE_ORDER",
  "reference_id": 1,
  "remarks": "Stock received",
  "before_stock": 10.0,
  "after_stock": 15.0,
  "created_at": "2026-05-18T10:00:00"
}
```

| Method | Endpoint | Auth | Body | Response |
| --- | --- | --- | --- | --- |
| `POST` | `/stock-transactions/` | Yes | Stock transaction create body | `StockTransaction` |
| `GET` | `/stock-transactions/` | Yes | None | `[StockTransaction]` |
| `GET` | `/stock-transactions/product/{product_id}` | Yes | None | `[StockTransaction]` |

Possible errors:

- `400`: `Insufficient stock`
- `400`: `Invalid transaction type`
- `404`: `Product not found`

## Data Type Notes

- `UUID` values are strings, for example `550e8400-e29b-41d4-a716-446655440000`.
- `date` values use `YYYY-MM-DD`.
- `datetime` values use ISO 8601 format, for example `2026-05-18T10:00:00`.
- Decimal fields can be sent as JSON numbers.
- Fields marked optional in schemas may be omitted or sent as `null`.

## Route Coverage Summary

| Module | Endpoints |
| --- | ---: |
| Root | 1 |
| Authentication | 7 |
| Vendors | 5 |
| Customers | 5 |
| Cashbook | 5 |
| Purchase Orders | 4 |
| Bills | 5 |
| Quotations | 5 |
| Sales Orders | 5 |
| Sales Invoices | 5 |
| Inventory Categories | 5 |
| Inventory Units | 5 |
| Inventory Products | 5 |
| Warehouses | 5 |
| Stock Transactions | 3 |


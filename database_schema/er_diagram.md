# Entity Relationship Diagram (ERD)

## Database Relationships Overview

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ full_name       │
│ hashed_password │
│ role            │
│ is_active       │
│ created_at      │
└─────────────────┘
         │
         ├─────────┬──────────┐
         │         │          │
         │         │          │
    ┌────▼────┐ ┌─▼──────┐ ┌─▼────────┐
    │ SALES   │ │EXPENSES│ │PURCHASES │
    └────┬────┘ └────────┘ └─────┬────┘
         │                        │
    ┌────▼─────────┐         ┌────▼─────────────┐
    │ SALE_ITEMS   │         │ PURCHASE_ITEMS  │
    └────┬─────────┘         └────┬─────────────┘
         │                         │
         │                    ┌────▼────────┐
         │                    │  PRODUCTS   │
         │                    └────┬────────┘
         │                         │
         │                    ┌────▼─────────┐
         │                    │ CATEGORIES   │
         │                    └──────────────┘
         │
         │
    ┌────▼──────────┐
    │  CUSTOMERS    │
    └───────────────┘
         │
    ┌────▼──────────┐
    │  INVOICES     │
    └───────────────┘


┌──────────────┐
│  SUPPLIERS   │
└──────────────┘
         │
    ┌────▼─────────┐
    │  PRODUCTS    │
    └──────────────┘
```

## Detailed Relationships

### 1. Users Table
- **Role**: Central authentication and authorization
- **Relationships**:
  - One User → Many Sales (user_id in sales)
  - One User → Many Purchases (user_id in purchases)
  - One User → Many Expenses (user_id in expenses)

### 2. Products Table
- **Role**: Central inventory management
- **Relationships**:
  - One Category → Many Products (category_id in products)
  - One Supplier → Many Products (supplier_id in products)
  - One Product → Many SaleItems (product_id in sale_items)
  - One Product → Many PurchaseItems (product_id in purchase_items)

### 3. Sales Flow
- **One Customer → Many Sales**
- **One Sale → Many SaleItems**
- **One SaleItem → One Product**
- **One Sale → One Invoice**

### 4. Purchase Flow
- **One Supplier → Many Purchases**
- **One Purchase → Many PurchaseItems**
- **One PurchaseItem → One Product**

### 5. Expenses
- **One User → Many Expenses**
- **No direct relationship to other entities**

### 6. Invoices
- **One Customer → Many Invoices**
- **One Sale → One Invoice**

## Data Flow Examples

### Sales Transaction Flow
```
1. Customer places order
   Customers → Sales (created)
   
2. Items added to sale
   Products → SaleItems (created)
   SaleItems → Sales (linked)
   
3. Stock reduced
   Products.quantity -= sold_quantity
   
4. Invoice generated
   Sales → Invoices (created)
   
5. Customer receives invoice
   Invoices sent to Customers
```

### Purchase Transaction Flow
```
1. Purchase order created
   Suppliers → Purchases (created)
   
2. Line items added
   Products → PurchaseItems (created)
   PurchaseItems → Purchases (linked)
   
3. Stock increases on receipt
   Products.quantity += received_quantity
   
4. Payment tracked
   Purchases marked as received
```

### Inventory Management
```
Current_Stock = Initial_Stock + Purchases - Sales

When Sale Created:
  Products.quantity -= SaleItems.quantity
  
When Purchase Received:
  Products.quantity += PurchaseItems.quantity_received
```
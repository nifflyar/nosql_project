# SWAGSTORE — Clothing Store Web Application

## **Project — Advanced Databases (NoSQL)**

---

## Project Overview

**SWAGSTORE** is a full-stack web application representing an online clothing store.  

The application demonstrates:
- advanced MongoDB data modeling
- real business logic
- aggregation pipelines
- authentication & authorization
- RESTful API design
- frontend–backend integration

The system supports both **customers** and **administrators**, allowing full management of products, orders, and analytical statistics.

---

## System Architecture

### Overall Architecture


```scss
┌─────────────┐      HTTP (REST)     ┌──────────────┐
│   Frontend  │  ─────────────────▶  │   Backend    │
│   React     │                      │   FastAPI    │
└─────────────┘                      └──────────────┘
                                            │
                                            │ MongoDB (Motor)
                                            ▼
                                     ┌──────────────┐
                                     │   MongoDB    │
                                     └──────────────┘
```


---

### Technologies Used

| Layer       | Technology |
|------------|------------|
| Frontend   | React (Vite) |
| Backend    | FastAPI |
| Database   | MongoDB |
| Driver     | Motor (async MongoDB driver) |
| Auth       | JWT |
| API Docs   | Swagger / OpenAPI |
| Deployment | Docker |

---

## Database Schema Description

### Collections Overview

| Collection  | Purpose |
|------------|--------|
| `users` | Store users and roles |
| `categories` | Product categories |
| `products` | Products with embedded variants |
| `orders` | Orders with embedded order items |

---

### Users Collection

```json
{
  "_id": ObjectId,
  "name": "string",
  "email": "string",
  "address": "string",
  "role": "admin | customer",
  "passwordHash": "string",
  "created_at": "datetime"
}
```

#### Referenced by orders (user_id)
#### Used for authentication and authorization

---

### Categories Collection

```json
{
  "_id": ObjectId,
  "name": "string",
  "description": "string",
  "created_at": "datetime"
}
```

---

### Products Collection (Embedded Model)

```json
{
  "_id": ObjectId,
  "name": "string",
  "price": number,
  "category_id": ObjectId,
  "image_url": "string",
  "variants": [
    {
      "size": "XS | S | M | L | XL",
      "color": "string",
      "stock": number
    }
  ],
  "created_at": "datetime"
}
```

#### Variants are embedded for faster reads
#### Stock managed via $inc and positional operators

---


### Orders Collection (Embedded Items)

```json
{
  "_id": ObjectId,
  "user_id": ObjectId,
  "status": "pending | shipped | delivered | canceled",
  "items": [
    {
      "product_id": ObjectId,
      "name": "string",
      "price": number,
      "quantity": number,
      "variant": {
        "size": "string",
        "color": "string"
      }
    }
  ],
  "total": number,
  "created_at": "datetime"
}
```

#### Embedded order items
#### Business logic applied on order status changes


---

## MongoDB Queries & Aggregations

### Sales by Category
```js
$unwind -> $lookup -> $group -> $lookup -> $project -> $sort
```
#### Returns:
- #### total revenue per category
- #### total items sold

--- 

### Revenue by Month
```js
$group (year, month) -> $project -> $sort
```
#### Returns:
- #### monthly revenue
- #### number of orders per month

---
### Top Products
```js
$unwind -> $group -> $lookup -> $project -> $sort -> $limit
```
#### Returns:
- #### most sold products by quantity
- #### revenue per product

---
## Authentication & Authorization

### JWT-based authentication

### Role-based access:
- Admin: full access (CRUD, statistics, status changes)
- Customer: own orders only

### Protected endpoints use dependency injection:
```python
admin: AdminDep
```

---
## REST API Documentation

### Core Endpoints

#### Products
- GET /products
- POST /products (admin)
- PATCH /products/{id} (admin)
- DELETE /products/{id} (admin)

#### Orders
- POST /orders
- GET /orders/my
- POST /orders/{id}/cancel
- POST /orders/{id}/{status} (admin)

#### Statistics (Admin only)
- GET /stats/sales-by-category
- GET /stats/revenue-by-month
- GET /stats/top-products

#### All endpoints are documented via Swagger UI.

---

## Advanced MongoDB Operations

### The project uses:
- $set
- $push
- $pull
- $inc
- positional $
- multi-stage aggregation pipelines
- embedded + referenced models

---

## Indexing & Optimization Strategy

### To improve query and aggregation performance, the following indexes were created based on real application usage.

```js
users: { email: 1 }           
users: { role: 1 }

categories: { name: 1 }

products: { category_id: 1 }
products: { price: 1 }
products: { "variants.size": 1, "variants.color": 1 }

orders: { user_id: 1 }
orders: { status: 1 }
orders: { created_at: -1 }
```

### Benefits:
- faster filtering
- efficient order queries
- optimized statistics aggregation

---
## Frontend Functionality

### Implemented Pages
- Home
- Shop (filters + search)
- Cart
- Login / Register
- Orders
- Admin Dashboard
- Admin Products
- Admin Orders
- Statistics

### Frontend supports:
- real HTTP requests
- filtering
- searching
- cart logic
- admin management


---

## Running the Project (Docker)
```bash
docker-compose up --build
```

Frontend
```arduino
http://localhost:5173
```

Backend
```arduino
http://localhost:8000
```

Swagger
```arduino
http://localhost:8000/docs
```

--- 

## Team Contribution
### Student:
- Backend architecture
- MongoDB schema design
- Aggregation pipelines
- REST API implementation
- Frontend integration
- Docker configuration
- Documentation
#### (Single-student project)


--- 

## Conclusion
### SWAGSTORE is a complete NoSQL-based web application featuring:
- real-world business logic
- advanced MongoDB usage
- clean backend architecture
- functional frontend
- production-ready structure
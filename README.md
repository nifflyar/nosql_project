# SWAGSTORE – Clothing Store Web Application

## Project Overview
SWAGSTORE is a full-stack web application developed as an endterm project for the course
**Advanced Databases (NoSQL)**.  
The system represents an online clothing store with product catalog, shopping orders,
admin management, and analytical statistics.

The project demonstrates advanced MongoDB usage including embedded documents,
aggregation pipelines, and business-oriented backend logic.

---

## Tech Stack
**Backend**
- Python (FastAPI)
- MongoDB (Motor async driver)
- JWT Authentication

**Frontend**
- React (Vite)
- Axios

---

## Features
- User authentication and authorization (Admin / Customer)
- Product and category management
- Order creation and status tracking
- Advanced MongoDB aggregation statistics
- Admin dashboard with real-time data

---

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
# nosql_project

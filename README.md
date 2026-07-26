# ⚡ Lumen API — Modern E-commerce Backend

FastAPI-based REST API for online store. Built for speed and scalability.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.140-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

### 🚀 Live Docs
After running, open: `http://127.0.0.1:8000/docs` — interactive Swagger UI

### ✨ Features
- CRUD for products
- Category filtering
- SQLite + auto-seed data
- Auto-generated Swagger docs
- Stats endpoint

### 📦 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Welcome |
| GET | /api/products | List all products |
| GET | /api/products/{id} | Get product by ID |
| POST | /api/products | Create product |
| DELETE | /api/products/{id} | Delete product |
| GET | /api/stats | Store statistics |

### 🛠 Quick Start
```bash
pip install -r requirements.txt
uvicorn main:app --reload

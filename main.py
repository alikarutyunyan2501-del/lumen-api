from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

app = FastAPI(title="Lumen API", description="Modern e-commerce backend", version="1.0.0")

def init_db():
    conn = sqlite3.connect('lumen.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, category TEXT, image TEXT, created TIMESTAMP)''')
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            ("iPhone 15 Pro", 99990, "electronics", "iphone.jpg"),
            ("Nike Air Max", 12990, "fashion", "nike.jpg"),
            ("MacBook Air M3", 129990, "electronics", "macbook.jpg"),
            ("KoKo Hoodie", 4990, "fashion", "hoodie.jpg"),
        ]
        for p in products:
            c.execute("INSERT INTO products (name, price, category, image, created) VALUES (?,?,?,?,?)", (*p, datetime.now()))
    conn.commit()
    conn.close()

init_db()

class Product(BaseModel):
    id: int
    name: str
    price: int
    category: str
    image: str

class ProductCreate(BaseModel):
    name: str
    price: int
    category: str
    image: str = "default.jpg"

@app.get("/")
def root():
    return {"message": "Welcome to Lumen API", "docs": "/docs"}

@app.get("/api/products")
def get_products(category: str = None):
    conn = sqlite3.connect('lumen.db')
    c = conn.cursor()
    if category:
        c.execute("SELECT * FROM products WHERE category=?", (category,))
    else:
        c.execute("SELECT * FROM products")
    rows = c.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "price": r[2], "category": r[3], "image": r[4]} for r in rows]

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    conn = sqlite3.connect('lumen.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": row[0], "name": row[1], "price": row[2], "category": row[3], "image": row[4]}

@app.post("/api/products")
def create_product(product: ProductCreate):
    conn = sqlite3.connect('lumen.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, price, category, image, created) VALUES (?,?,?,?,?)",
              (product.name, product.price, product.category, product.image, datetime.now()))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return {**product.dict(), "id": new_id}

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    conn = sqlite3.connect('lumen.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted", "id": product_id}

@app.get("/api/stats")
def get_stats():
    conn = sqlite3.connect('lumen.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(price) FROM products")
    count, total = c.fetchone()
    conn.close()
    return {"total_products": count, "total_value": total, "currency": "RUB"}

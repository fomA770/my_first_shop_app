#main.py
from fastapi import FastAPI
from app.core.database import lifespan
from app.routers import auth, products, cart, orders

app = FastAPI(title="Shop API", lifespan=lifespan)
app.include_router(auth.router, prefix="/auth")
app.include_router(products.router, prefix="/products")
app.include_router(cart.router, prefix="/cart")
app.include_router(orders.router, prefix="/orders")

@app.get("/")
async def root():
    return {"message": "Shop API is running"}
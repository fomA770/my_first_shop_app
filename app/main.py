from fastapi import FastAPI
from pathlib import Path
from app.core.database import lifespan
from app.routers import auth, products, cart, orders, users
from app.core.logging import setup_logging
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Shop API", 
    lifespan=lifespan,
    description="Shop_app_API",
    version="1.0.0",
    contact={"name": "Max Pronichev"},
    terms_of_service="https://localhost:8000/terms",
    openapi_tags=[
        {"name": "auth", "description": "Registration and authentification"},
        {"name": "product", "description": "Product management"},
        {"name": "cart", "description": "Manage items in cart"},
        {"name": "orders", "description": "Create / edit orders"}
    ]
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/auth")
app.include_router(products.router, prefix="/products")
app.include_router(cart.router, prefix="/cart")
app.include_router(orders.router, prefix="/orders")
app.include_router(users.router, prefix="/users")

setup_logging()

FRONTEND_PATH = Path(__file__).parent / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND_PATH)), name="static")

@app.get("/")
async def root():
    index_page_path = FRONTEND_PATH / "index.html"
    if index_page_path.exists():
        return FileResponse(index_page_path)
    return JSONResponse({"error": "index.html not found"}, status_code=404)
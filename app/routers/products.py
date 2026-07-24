#products.py
from fastapi import APIRouter
from app.schemas.schemas import ProductRead, ProductCreate, ProductBulkCreate, ProductFilters
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_products import products_crud
from fastapi import Depends
from app.core.database import get_db
from typing import Optional
from app.core.dependencies import require_admin, require_admin_or_manager

router = APIRouter(
    tags=["Products"]
)

@router.get("/get_all") #admin
async def handle_get_all_products(db: AsyncSession = Depends(get_db),
                                  is_admin: bool = Depends(require_admin),
                                    skip: int = 0,
                                    limit: int = 10,
                                    filters: ProductFilters = Depends()):
    products = await products_crud.get_all_products(db=db, skip=skip, limit=limit, filters=filters)
    return products

@router.post("/create") #admin + manager
async def handle_create_product(product: ProductCreate, 
                                db: AsyncSession = Depends(get_db),
                                is_admin_or_manager: bool = Depends(require_admin_or_manager)):
    result = await products_crud.create_product(db=db, product=product)
    return result

@router.post("/create_many") #admin + manager
async def handle_create_products(product_dict: ProductBulkCreate, 
                                 db: AsyncSession = Depends(get_db),
                                 is_admin_or_manager: bool = Depends(require_admin_or_manager)):
    result = await products_crud.create_products(db=db, product_dict=product_dict)
    return result

@router.put("/del/{product_id}") #admin
async def handle_del_product(product_id: int, 
                             db: AsyncSession = Depends(get_db),
                             is_admin: bool = Depends(require_admin)):
    result = await products_crud.del_product(db=db, product_id=product_id)
    return result # TODO
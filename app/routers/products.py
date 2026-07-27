#products.py
from fastapi import APIRouter, HTTPException
from app.schemas.schemas import ProductRead, ProductCreate, ProductBulkCreate, ProductFilters, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_products import products_crud
from fastapi import Depends
from app.core.database import get_db
from typing import Optional, List
from app.core.dependencies import require_admin, require_admin_or_manager
from app.models.models import User

router = APIRouter(
    tags=["Products"]
)

@router.get("/get_all",
            summary="Get all products",
            description="Get a list of all products with filters and pagination",
            response_model=List[ProductRead]) #admin
async def handle_get_all_products(db: AsyncSession = Depends(get_db),
                                    skip: int = 0,
                                    limit: int = 10,
                                    filters: ProductFilters = Depends()):
    products = await products_crud.get_all_products(db=db, skip=skip, limit=limit, filters=filters)
    return products

@router.post("/create") #admin + manager
async def handle_create_product(product: ProductCreate, 
                                db: AsyncSession = Depends(get_db),
                                user: User = Depends(require_admin_or_manager)):
    result = await products_crud.create_product(db=db, product=product)
    return result

@router.post("/create_many") #admin + manager
async def handle_create_products(product_dict: ProductBulkCreate, 
                                 db: AsyncSession = Depends(get_db),
                                 user: User = Depends(require_admin_or_manager)):
    result = await products_crud.create_products(db=db, product_dict=product_dict)
    return result

@router.delete("/del/{product_id}") #admin
async def handle_del_product(product_id: int, 
                             db: AsyncSession = Depends(get_db),
                             user: User = Depends(require_admin)) -> ProductRead:
    try:
        result = await products_crud.del_product(db=db, product_id=product_id)
        return ProductRead.model_validate(result)
    except ValueError as e:
        raise HTTPException(422, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.put("/update/{product_id}") # admin + manager
async def handle_update_product(product_id: int,
                                product_data: ProductUpdate,
                                db: AsyncSession = Depends(get_db),
                                user: User = Depends(require_admin_or_manager)):
    try:
        result = await products_crud.update_product(product_id=product_id, product_data=product_data, db=db)
        return result
    except ValueError as e:
        raise HTTPException(401, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))


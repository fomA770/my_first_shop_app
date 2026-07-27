#crud_products.py
from sqlalchemy import select, text, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Product, OrderItem
from app.crud.base import CRUDBase
from app.schemas.schemas import ProductRead, ProductCreate, ProductBulkCreate, ProductFilters, ProductUpdate
from typing import Optional
from fastapi import HTTPException, status

class CRUDProducts(CRUDBase):
    def __init__(self):
        super().__init__(Product)

    async def get_all_products(self, db: AsyncSession,
                               skip: int = 0,
                               limit: int = 10,
                               filters: Optional[ProductFilters] = None
                               ) -> list[ProductRead]:
        query = select(Product)
        if filters:
            if filters.category is not None:
                query = query.where(Product.category == filters.category)
            if filters.max_price is not None:
                query = query.where(Product.price <= filters.max_price)
            if filters.min_price is not None:
                query = query.where(Product.price >= filters.min_price)
            if filters.in_stock is not None:
                query = query.where(Product.storage_count > 0)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)

        # count_query = select(func.count()).select_from(query.subquery())
        # total = await db.scalar(count_query)
        # result = await db.execute(
        #     text("""
        #         SELECT * FROM products OFFSET :skip LIMIT :limit;
        #         """), params={"skip": skip, "limit": limit}
        # )
        
        rows = result.scalars().all()
        return [ProductRead.model_validate(row) for row in rows]

    async def create_product(self, db: AsyncSession,
                             product: ProductCreate):
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            storage_count=product.storage_count,
            category=product.category
        )

        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return ProductRead.model_validate(new_product)

    async def create_products(self, db: AsyncSession,
                              product_dict: ProductBulkCreate):
        new_products = []
        for product in product_dict.products:
            new_product = Product(
                name=product.name,
                description=product.description,
                price=product.price,
                storage_count=product.storage_count,
                category=product.category
            )
            db.add(new_product)
            new_products.append(new_product)
        await db.commit()
        for p in new_products:
            await db.refresh(p)

        return [ProductRead.model_validate(p) for p in new_products]

    async def del_product(self, db: AsyncSession, product_id: int):
        look_in_order_items_query = select(OrderItem).where(OrderItem.product_id == product_id)
        result = await db.execute(look_in_order_items_query)
        used_products = result.scalar_one_or_none()
        if used_products:
            raise ValueError("Product is already used in orders")
        product = await self.get(db=db, obj_id=product_id)
        if not product:
            raise ValueError("Product doesn't exist")
        await db.delete(product)
        await db.commit()

        return ProductRead.model_validate(product)

    async def update_product(self, db: AsyncSession, product_id: int, product_data: ProductUpdate):
        product = await self.get(db=db, obj_id=product_id)
        if not product:
            raise ValueError("Product doesn't exist")
        update_data = product_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(product, key, value)

        await db.commit()
        await db.refresh(product)
        return product

products_crud = CRUDProducts()
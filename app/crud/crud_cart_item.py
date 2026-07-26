from app.crud.base import CRUDBase
from app.models.models import Cart, Product, CartItem, OrderItem, Order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.schemas.schemas import CartReturn, CartItemReturn
from typing import Optional, List, Sequence
from app.crud.crud_products import products_crud


class CRUDCartItem(CRUDBase):
    def __init__(self):
        super().__init__(CartItem)

    async def get_all_cart_items(self, cart_id: int, db: AsyncSession) -> Sequence[CartItem]:
        "Получаем все товары в корзине"
        result = await db.execute(select(self.model).where(self.model.cart_id == cart_id))
        items = result.scalars().all()
        return items


    async def get_by_cart_and_product(self, cart_id: int, product_id: int, db: AsyncSession) -> Optional[CartItem]:
        """Получить позицию корзины по cart_id и product_id"""
        result = await db.execute(
            select(self.model)
            .where(
                and_(
                    self.model.cart_id == cart_id,
                    self.model.product_id == product_id
                )
            )
            .options(selectinload(self.model.product))
        )
        return result.scalar_one_or_none()
    

cart_item_crud = CRUDCartItem()

from app.crud.base import CRUDBase
from app.models.models import Cart, Product, CartItem, OrderItem, Order
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.schemas.schemas import CartReturn, CartItemReturn
from typing import Optional, List, Sequence
from app.crud.crud_products import products_crud
from app.crud.crud_cart_item import cart_item_crud


class CRUDCart(CRUDBase):
    def __init__(self):
        super().__init__(Cart)

    async def get_cart(self, user_id: int, db: AsyncSession):
        query_result = await db.execute(select(self.model).where(self.model.user_id == user_id))
        cart = query_result.scalar_one_or_none()
        if cart is None:
            cart = Cart(user_id=user_id)
            db.add(cart)
            await db.commit()
            await db.refresh(cart)
        return cart

    async def add_to_cart(self, user_id: int, product_id: int, cart_id: int, quantity: int, db: AsyncSession):
        "Добавить в корзину товар по id юзера и id продукта (с указанным количеством)"
        cart = await self.get_cart(user_id=user_id, db=db)
        product = await products_crud.get(db=db, obj_id=product_id)
        print(product)
        if product is None:
            raise ValueError("Product doesn't exist")
        if product.storage_count == 0 or quantity > product.storage_count:
            raise ValueError("Product is out of stock")
        cart_item = await cart_item_crud.get_by_cart_and_product(cart_id=cart_id, product_id=product_id, db=db)
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity
            )
            db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        return cart_item

    async def del_by_id(self, user_id: int, product_id: int, db: AsyncSession) -> Optional[CartItem]:
        "Удалить товар (все товары с этим id) из корзины по id товара и id пользователя"
        cart = await self.get_cart(user_id=user_id, db=db)
        if cart is None:
            raise ValueError("User has nothing in cart")
        query = select(CartItem).where((CartItem.cart_id == cart.id) & (CartItem.product_id == product_id))
        result = await db.execute(query)
        cart_item = result.scalar_one_or_none()
        if not cart_item:
            raise ValueError("No product found")
        await db.delete(cart_item)
        await db.commit()
        return cart_item

    async def clear_cart(self, cart_id: int, db: AsyncSession) -> Optional[Sequence[CartItem]]:
        cart_items = await cart_item_crud.get_all_cart_items(cart_id=cart_id, db=db)
        for item in cart_items:
            await db.delete(item)
        await db.commit()
        return cart_items


        


cart_crud = CRUDCart()
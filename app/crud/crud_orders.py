from app.crud.base import CRUDBase
from app.models.models import OrderStatus, Product, CartItem, OrderItem, Order, User, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, func
from sqlalchemy.orm import selectinload, joinedload
from typing import Optional, List, Sequence
from app.crud.crud_cart import cart_crud
from app.crud.crud_cart_item import cart_item_crud

class CRUDOrders(CRUDBase):
    def __init__(self):
        super().__init__(Order)

    async def create_order(self, user_id: int, db: AsyncSession):
        cart = await cart_crud.get_cart(user_id=user_id, db=db)
        query_for_cart_items = (
            select(CartItem.product_id, 
                   Product.name, 
                   Product.price, 
                   CartItem.quantity, 
                   (CartItem.quantity * Product.price).label("subtotal"))
            .join(CartItem.product)
            .where(CartItem.cart_id == cart.id)
        )
        query_for_total_amount = (
            select(func.sum(CartItem.quantity * Product.price))
            .join(CartItem.product)
            .where(CartItem.cart_id == cart.id)
        )
        query_for_total_amount_result = await db.execute(query_for_total_amount)
        query_for_cart_items_result = await db.execute(query_for_cart_items)
        total_amount = query_for_total_amount_result.scalar() or 0.0
        cart_items = query_for_cart_items_result.all()
        if not cart_items:
            raise ValueError("Cart is empty")
        
        await cart_crud.clear_cart(cart_id=cart.id, db=db)
        new_order = Order(
            total_amount=total_amount,
            user_id=user_id
        )
        db.add(new_order)
        await db.flush()
        await db.refresh(new_order)
        order_items = []
        for cart_item in cart_items:
            product = await db.get(Product, cart_item.product_id)
            if not product:
                raise ValueError("Product doesn't exist")
            if product.storage_count >= cart_item.quantity:
                product.storage_count -= cart_item.quantity
            db.add(product)
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=cart_item.product_id,
                product_name=cart_item.name,
                product_price=cart_item.price,
                quantity=cart_item.quantity,
                total_price=cart_item.subtotal

            )
            db.add(order_item)
            order_items.append(order_item)
        await db.commit()
        for item in order_items:
            await db.refresh(item)
        return new_order, order_items

    async def get_user_orders_items(self, user_id: int, db: AsyncSession):
        query = (
            select(OrderItem.product_id, OrderItem.quantity, OrderItem.order_id, Order.status.label("order_status"))
            .join(OrderItem.order)
            .join(Order.user)
            .where(User.id == user_id)
        )
        result = await db.execute(query)
        user_orders_items = result.all()
        return user_orders_items

    async def update_order_status(self, order_id: str, status: OrderStatus, db: AsyncSession):
        query = (
            select(Order).where(Order.id == order_id)
        )
        result = await db.execute(query)
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError("No order with such id")
        
        order.status = status

        await db.commit()
        await db.refresh(order)
        return order

orders_crud = CRUDOrders()

        
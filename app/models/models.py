#models.py
from datetime import datetime
from typing import Optional, List
from enum import Enum
from decimal import Decimal
from sqlalchemy.orm import (Mapped, mapped_column, relationship, 
                            DeclarativeBase, validates)
from sqlalchemy import (String, Boolean, DateTime, Table, ForeignKey, 
                        Column, text, func, Numeric, Integer, Enum as SAEnum)

class OrderStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True, nullable=False),
    Column("role_id", ForeignKey("roles.id"), primary_key=True, nullable=False),
)

class User(Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(150), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        #insert_default=text("NOW()"),
        nullable=False)
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        #insert_default=func.now(),
        onupdate=text("NOW()"), 
        nullable=False)

    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
        lazy="selectin",
        order_by="Role.name"
    )

    cart: Mapped["Cart"] = relationship("Cart", back_populates="user", uselist=False)
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"

class Role(Base):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    users: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin",
        order_by="User.email"
    )

    def __repr__(self) -> str:
        return f"<Role(id={self.id}, name={self.name})>"

class Product(Base):
    __tablename__ = "products"
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    storage_count: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(),
                                                 nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)

    order_items: Mapped["OrderItem"] = relationship("OrderItem", back_populates="product")
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="product")

class Cart(Base):
    __tablename__="carts"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="cart")
    items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart")

class CartItem(Base):
    __tablename__="cart_items"
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default = 1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")
    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")

    @validates('quantity')
    def validate_quantity(self, key, value):
        if value <= 0:
            raise ValueError("Необходимо указать количество товаров") #TODO change the error?
        return value

class Order(Base):
    __tablename__="orders"
    id: Mapped[str] = mapped_column(String(150), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__="order_items"
    order_id: Mapped[str] = mapped_column(String(150), ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    product_price: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer)
    total_price: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")



     
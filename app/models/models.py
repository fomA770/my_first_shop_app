#models.py
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Boolean, DateTime, Table, ForeignKey, Column, text, func, Numeric
from datetime import datetime, timezone
from typing import Optional, List

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
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

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(),
                                                 nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), 
                                                 server_default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)

     
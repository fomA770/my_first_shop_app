#schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer, Field
from datetime import datetime
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    roles: List[str]

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    storage_count: int
    category: str

class ProductBulkCreate(BaseModel):
    products: List[ProductCreate]

class ProductRead(ProductCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('created_at')
    def serialize_created_at(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @field_serializer('updated_at')
    def serialize_updated_at(self, dt: datetime) -> str:
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    storage_count: Optional[int] = None
    category: Optional[str] = None


class ProductFilters(BaseModel):
    """Фильтры для поиска товаров"""
    category: Optional[str] = Field(None, description="Фильтр по категории")
    max_price: Optional[float] = Field(None, ge=0, description="Максимальная цена")
    min_price: Optional[float] = Field(None, ge=0, description="Минимальная цена")
    in_stock: Optional[bool] = Field(None, description="Только в наличии")
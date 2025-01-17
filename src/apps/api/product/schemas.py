from typing import List

from pydantic import BaseModel
from src.apps.api.auth.schemas import DefaultDataSchema
from decimal import Decimal

from src.apps.api.category.schemas import CategorySchema


class CreateProductSchema(BaseModel):
    name: str
    price: Decimal
    image: str | None
    category_id: str


class ProductSchema(DefaultDataSchema, CreateProductSchema):
    category: CategorySchema


class UpdateProductSchema(BaseModel):
    name: str | None
    price: Decimal | None
    image: str | None


class PaginatedResponse(BaseModel):
    items: List[ProductSchema]
    total_count: int
    page: int
    page_size: int
    total_pages: int

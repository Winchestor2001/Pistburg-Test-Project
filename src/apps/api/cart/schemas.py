from pydantic import BaseModel
from src.apps.api.auth.schemas import DefaultDataSchema, ResponseUserSchema
from decimal import Decimal

from src.apps.api.product.schemas import ProductSchema


class CreateCartSchema(BaseModel):
    quantity: int
    product_id: str


class CartSchema(DefaultDataSchema, CreateCartSchema):
    product: ProductSchema
    user: ResponseUserSchema
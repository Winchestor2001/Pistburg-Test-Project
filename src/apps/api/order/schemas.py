from pydantic import BaseModel
from src.apps.api.auth.schemas import DefaultDataSchema, ResponseUserSchema
from decimal import Decimal

from src.apps.api.product.schemas import ProductSchema


class CreateOrderSchema(BaseModel):
    quantity: int
    product_id: str


class OrderSchema(DefaultDataSchema, CreateOrderSchema):
    product: ProductSchema
    user: ResponseUserSchema


class UpdateOrderSchema(BaseModel):
    quantity: int
    product: str
from pydantic import BaseModel
from src.apps.api.auth.schemas import DefaultDataSchema
from decimal import Decimal


class CreateProductSchema(BaseModel):
    name: str
    price: Decimal
    image: str | None


class ProductSchema(DefaultDataSchema, CreateProductSchema):
    pass


class UpdateProductSchema(BaseModel):
    name: str | None
    price: Decimal | None
    image: str | None
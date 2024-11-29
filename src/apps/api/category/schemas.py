from pydantic import BaseModel
from src.apps.api.auth.schemas import DefaultDataSchema


class CreateUpdateCategorySchema(BaseModel):
    name: str


class CategorySchema(DefaultDataSchema, CreateUpdateCategorySchema):
    pass
import logging
from typing import Annotated, List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.api.product import schemas
from src.apps.api.product.crud import create_product_obj, all_products_obj, get_single_product_obj, \
    update_product_data_obj, delete_product_obj
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/product", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductSchema)
async def add_product(
        product_data: schemas.CreateProductSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    new_product = await create_product_obj(session, **product_data.model_dump())
    return new_product


@router.get("/product", status_code=status.HTTP_200_OK, response_model=List[schemas.ProductSchema])
async def product_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    products = await all_products_obj(session)
    return products


@router.get("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=schemas.ProductSchema)
async def single_product(
        product_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    product = await get_single_product_obj(session, uuid=product_id)
    return product


@router.put("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=bool)
@router.patch("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def update_product(
        product_id: str,
        category_data: schemas.UpdateProductSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    updated_product = await update_product_data_obj(session, uuid=product_id, data=category_data.model_dump())
    return updated_product


@router.delete("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def delete_product(
        product_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    deleted_product = await delete_product_obj(session, uuid=product_id)
    return deleted_product

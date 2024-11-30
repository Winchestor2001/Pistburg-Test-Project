import logging
from typing import Annotated, List, Optional

from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

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


@router.get("/product", status_code=status.HTTP_200_OK, response_model=schemas.PaginatedResponse)
async def product_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        name: Optional[str] = Query(None, description="Filter products by name"),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(2, ge=1, le=100, description="Number of items per page"),
):
    products, total_count = await all_products_obj(session, name=name, page=page, page_size=page_size)
    return schemas.PaginatedResponse(
        items=products,
        total_count=total_count,
        page=page,
        page_size=page_size,
        total_pages=(total_count // page_size) + (1 if total_count % page_size != 0 else 0),
    )


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
        product_data: schemas.UpdateProductSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    updated_product = await update_product_data_obj(session, uuid=product_id, data=product_data.model_dump())
    return updated_product


@router.delete("/product/{product_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def delete_product(
        product_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    deleted_product = await delete_product_obj(session, uuid=product_id)
    return deleted_product

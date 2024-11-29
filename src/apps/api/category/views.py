import logging
from typing import Annotated, List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.api.category import schemas
from src.apps.api.category.crud import create_category_obj, all_categories_obj, get_single_category_obj, \
    update_category_data_obj, delete_category_obj
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/category", status_code=status.HTTP_201_CREATED, response_model=schemas.CategorySchema)
async def add_category(
        category_data: schemas.CreateUpdateCategorySchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    new_category = await create_category_obj(session, category_data.name)
    return new_category


@router.get("/categories", status_code=status.HTTP_200_OK, response_model=List[schemas.CategorySchema])
async def category_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    categories = await all_categories_obj(session)
    return categories


@router.get("/category/{category_id}", status_code=status.HTTP_200_OK, response_model=schemas.CategorySchema)
async def single_category(
        category_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    category = await get_single_category_obj(session, uuid=category_id)
    return category


@router.put("/category/{category_id}", status_code=status.HTTP_200_OK, response_model=bool)
@router.patch("/category/{category_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def update_category(
        category_id: str,
        category_data: schemas.CreateUpdateCategorySchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    updated_category = await update_category_data_obj(session, uuid=category_id, data=category_data.model_dump())
    return updated_category


@router.delete("/category/{category_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def delete_category(
        category_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    deleted_category = await delete_category_obj(session, uuid=category_id)
    return deleted_category
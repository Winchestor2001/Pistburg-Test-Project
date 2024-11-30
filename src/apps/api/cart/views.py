import logging
from typing import Annotated, List, Optional

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.api.auth.jwt_conf import JwtBearer
from src.apps.api.cart import schemas
from src.apps.api.cart.crud import create_cart_obj, all_carts_obj, delete_cart_obj
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/cart", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_201_CREATED)
async def add_cart(
        product_data: schemas.CreateCartSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        token: dict = Depends(JwtBearer())
):
    user_id = token["uuid"]
    new_cart_item = await create_cart_obj(session, **product_data.model_dump(), user_id=user_id)
    return new_cart_item


@router.get("/carts", status_code=status.HTTP_200_OK, response_model=List[schemas.CartSchema])
async def cart_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        token: dict = Depends(JwtBearer())
):
    user_id = token["uuid"]
    products = await all_carts_obj(session, user_id=user_id)
    return products


@router.delete("/cart/{cart_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def delete_cart(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        order_id: Optional[str] = None,
        token: dict = Depends(JwtBearer())
):
    user_id = token["uuid"]
    deleted_order = await delete_cart_obj(session, user_id=user_id, uuid=order_id)
    return deleted_order

import logging
from typing import Annotated, List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.api.auth.jwt_conf import JwtBearer
from src.apps.api.order import schemas
from src.apps.api.order.crud import create_order_obj, all_orders_obj, get_single_order_obj, \
    update_order_data_obj, delete_order_obj
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/order", dependencies=[Depends(JwtBearer())], status_code=status.HTTP_201_CREATED,
             response_model=schemas.OrderSchema)
async def add_order(
        product_data: schemas.CreateOrderSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        token: dict = Depends(JwtBearer())
):
    user_id = token["uuid"]
    new_product = await create_order_obj(session, **product_data.model_dump(), user_id=user_id)
    return new_product


@router.get("/orders", status_code=status.HTTP_200_OK, response_model=List[schemas.OrderSchema])
async def order_list(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    products = await all_orders_obj(session)
    return products


@router.get("/order/{order_id}", status_code=status.HTTP_200_OK, response_model=schemas.OrderSchema)
async def single_order(
        order_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    order = await get_single_order_obj(session, uuid=order_id)
    return order


@router.put("/order/{order_id}", status_code=status.HTTP_200_OK, response_model=bool)
@router.patch("/order/{order_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def update_order(
        order_id: str,
        order_data: schemas.UpdateOrderSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    updated_order = await update_order_data_obj(session, uuid=order_id, data=order_data.model_dump())
    return updated_order


@router.delete("/order/{order_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def delete_order(
        order_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    deleted_order = await delete_order_obj(session, uuid=order_id)
    return deleted_order

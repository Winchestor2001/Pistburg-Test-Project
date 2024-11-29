from decimal import Decimal

from sqlalchemy import select, and_, update, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db import Order, Product


async def create_order_obj(session: AsyncSession, quantity: int, product_id: str, user_id: str) -> Order:
    order_obj = Order(quantity=quantity, product_id=product_id, user_id=user_id)
    session.add(order_obj)
    await session.commit()
    return order_obj


async def all_orders_obj(session: AsyncSession) -> Sequence[Order] | None:
    stmt = select(Order).options(
        joinedload(Order.product).joinedload(Product.category),
        joinedload(Order.user))
    result = (await session.execute(stmt)).scalars().all()
    return result


async def get_single_order_obj(session: AsyncSession, uuid: str) -> Order | None:
    stmt = select(Order).where(Order.uuid == uuid).options(
        joinedload(Order.product).joinedload(Product.category),
        joinedload(Order.user))
    result = (await session.execute(stmt)).scalars().first()
    return result


async def update_order_data_obj(session: AsyncSession, data: dict, uuid: str) -> bool:
    filtered_data = {key: val for key, val in data.items() if val is not None}
    stmt = update(Order).where(Order.uuid == uuid).values(**filtered_data)

    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False


async def delete_order_obj(session: AsyncSession, uuid: str) -> bool:
    stmt = delete(Order).where(Order.uuid == uuid)
    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False
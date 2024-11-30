from decimal import Decimal

from sqlalchemy import select, and_, update, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db import Cart, Product


async def create_cart_obj(session: AsyncSession, quantity: int, product_id: str, user_id: str) -> Cart:
    cart_obj = Cart(quantity=quantity, product_id=product_id, user_id=user_id)
    session.add(cart_obj)
    await session.commit()
    return cart_obj


async def all_carts_obj(session: AsyncSession, user_id: str) -> Sequence[Cart] | None:
    stmt = select(Cart).where(Cart.user_id == user_id).options(
        joinedload(Cart.product).joinedload(Product.category),
        joinedload(Cart.user))
    result = (await session.execute(stmt)).scalars().all()
    return result


async def delete_cart_obj(session: AsyncSession, user_id: str, uuid: str = None) -> bool:
    if uuid:
        stmt = delete(Cart).where(and_(Cart.user_id == user_id, Cart.uuid == uuid))
    else:
        stmt = delete(Cart).where(Cart.user_id == user_id)
    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False
from decimal import Decimal

from sqlalchemy import select, and_, update, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import Product


async def create_product_obj(session: AsyncSession, name: str, price: Decimal, image: str | None) -> Product:
    product_obj = Product(name=name, price=price, image=image)
    session.add(product_obj)
    await session.commit()
    return product_obj


async def all_products_obj(session: AsyncSession) -> Sequence[Product] | None:
    stmt = select(Product)
    result = (await session.execute(stmt)).scalars().all()
    return result


async def get_single_product_obj(session: AsyncSession, uuid: str) -> Product | None:
    stmt = select(Product).where(Product.uuid == uuid)
    result = (await session.execute(stmt)).scalars().first()
    return result


async def update_product_data_obj(session: AsyncSession, data: dict, uuid: str) -> bool:
    filtered_data = {key: val for key, val in data.items() if val is not None}
    stmt = update(Product).where(Product.uuid == uuid).values(**filtered_data)

    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False


async def delete_product_obj(session: AsyncSession, uuid: str) -> bool:
    stmt = delete(Product).where(Product.uuid == uuid)
    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False
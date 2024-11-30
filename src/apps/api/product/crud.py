from decimal import Decimal
from typing import Optional

from sqlalchemy import select, and_, update, Sequence, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db import Product


async def create_product_obj(session: AsyncSession, name: str, category_id: str, price: Decimal,
                             image: str | None) -> Product:
    product_obj = Product(name=name, price=price, image=image, category_id=category_id)
    session.add(product_obj)
    await session.commit()
    return product_obj


async def all_products_obj(session: AsyncSession, name: Optional[str], page: int, page_size: int) -> Sequence[
                                                                                                         Product] | None:
    stmt = select(Product).options(joinedload(Product.category))
    if name:
        stmt = stmt.where(Product.name.ilike(f"%{name}%"))

    count_stmt = select(func.count()).select_from(Product)
    if name:
        count_stmt = count_stmt.where(Product.name.ilike(f"%{name}%"))

    total_count = (await session.execute(count_stmt)).scalar()

    stmt = stmt.offset((page - 1) * page_size).limit(page_size)

    result = (await session.execute(stmt)).scalars().all()

    return result, total_count


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

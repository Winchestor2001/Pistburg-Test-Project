from sqlalchemy import select, and_, update, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import Category


async def create_category_obj(session: AsyncSession, name: str) -> Category:
    category_obj = Category(name=name)
    session.add(category_obj)
    await session.commit()
    return category_obj


async def all_categories_obj(session: AsyncSession) -> Sequence[Category] | None:
    stmt = select(Category)
    result = (await session.execute(stmt)).scalars().all()
    return result


async def get_single_category_obj(session: AsyncSession, uuid: str) -> Category | None:
    stmt = select(Category).where(Category.uuid == uuid)
    result = (await session.execute(stmt)).scalars().first()
    return result


async def update_category_data_obj(session: AsyncSession, data: dict, uuid: str) -> bool:
    filtered_data = {key: val for key, val in data.items() if val is not None}
    stmt = update(Category).where(Category.uuid == uuid).values(**filtered_data)

    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False


async def delete_category_obj(session: AsyncSession, uuid: str) -> bool:
    stmt = delete(Category).where(Category.uuid == uuid)
    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False
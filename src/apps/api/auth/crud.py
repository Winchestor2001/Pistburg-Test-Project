from sqlalchemy import select, and_, update, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.api.auth.jwt_conf import hash_password
from src.db import User


async def check_username_obj(session: AsyncSession, username: str) -> bool | None:
    stmt = select(User).where(User.username == username)
    result = await session.scalar(stmt)
    return result


async def check_verification_code_obj(session: AsyncSession, username: str, code: str) -> bool | None:
    stmt = select(User).filter(and_(User.username == username, User.verification_code == code))
    result = await session.scalar(stmt)
    return result


async def create_user_obj(session: AsyncSession, full_name: str, username: str, password: str) -> User:
    hashed_password = await hash_password(password=password)
    user_obj = User(full_name=full_name, username=username, password=hashed_password)
    user_obj.generate_verification_code()
    session.add(user_obj)
    await session.commit()
    return user_obj


async def update_user_data_obj(session: AsyncSession, data: dict, username: str = None, uuid: str = None) -> bool:
    filtered_data = {key: val for key, val in data.items() if val is not None}
    if username:
        stmt = update(User).where(User.username == username).values(**filtered_data)
    else:
        stmt = update(User).where(User.uuid == uuid).values(**filtered_data)

    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False


async def get_user_data_obj(session: AsyncSession, username: str = None, uuid: str = None) -> User | None:
    if username:
        stmt = select(User).where(User.username == username)
    else:
        stmt = select(User).where(User.uuid == uuid)
    result = (await session.execute(stmt)).scalars().first()
    return result


async def get_all_users_data_obj(session: AsyncSession) -> Sequence[User] | None:
    stmt = select(User)
    result = (await session.execute(stmt)).scalars().all()
    return result


async def delete_user_obj(session: AsyncSession, uuid: str) -> bool:
    stmt = delete(User).where(User.uuid == uuid)
    result = await session.execute(stmt)
    if result:
        await session.commit()
        return True
    else:
        return False
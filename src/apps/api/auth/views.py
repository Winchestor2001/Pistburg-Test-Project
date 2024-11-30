import logging
from http.client import HTTPException
from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.apps.api import exceptions
from src.apps.api.auth import schemas
from src.apps.api.auth.crud import create_user_obj, check_username_obj, check_verification_code_obj, \
    update_user_data_obj, get_user_data_obj, get_all_users_data_obj, delete_user_obj
from src.apps.api.auth.jwt_conf import verify_password, JwtBearer
from src.apps.api.auth.utils import role_check
from src.db import db_helper

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUserSchema)
async def registration_user(
        registration_data: schemas.RegistrationUserSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    if not await check_username_obj(session, registration_data.username):
        new_user = await create_user_obj(session, **registration_data.model_dump())
        return new_user
    raise exceptions.username_already_exists


@router.post("/verification", status_code=status.HTTP_200_OK, response_model=schemas.ResponseUserSchema)
async def verification_user(
        verification_data: schemas.VerificationUserSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    checking = await check_verification_code_obj(session, **verification_data.model_dump())
    if checking:
        await update_user_data_obj(session, username=verification_data.username,
                                                  data={"is_verified": True})
        new_data = await get_user_data_obj(session, username=verification_data.username)
        return new_data
    raise exceptions.verification_code_incorrect


@router.post("/authentication", status_code=status.HTTP_200_OK)
async def authentication_user(
        authentication_data: schemas.AuthenticationUserSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter),]
):
    user_data = await get_user_data_obj(session, authentication_data.username)

    checking = await verify_password(authentication_data.password, user_data.password)
    if checking:
        return JwtBearer.create_tokens(user_data.uuid)
    raise exceptions.authentication_incorrect


@router.get("/me", status_code=status.HTTP_200_OK, dependencies=[Depends(JwtBearer())],
            response_model=schemas.ResponseUserSchema)
async def user_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        token: dict = Depends(JwtBearer())
):
    user_id = token["uuid"]
    user_data = await get_user_data_obj(session, uuid=user_id)
    if user_data:
        return user_data
    raise exceptions.authentication_incorrect


@router.get("/users", status_code=status.HTTP_200_OK,
            dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=List[schemas.ResponseUserSchema])
async def all_users_info(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    users_data = await get_all_users_data_obj(session)
    return users_data


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=schemas.ResponseUserSchema)
async def single_user_info(
        user_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    user_data = await get_user_data_obj(session, uuid=user_id)
    if user_data:
        return user_data
    raise exceptions.user_not_found


@router.put("/user/{user_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=schemas.ResponseUserSchema)
@router.patch("/user/{user_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=schemas.ResponseUserSchema)
async def put_user_info(
        user_id: str,
        data: schemas.UpdateUserDataSchema,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    put_data = await update_user_data_obj(session, data=data.model_dump(), uuid=user_id)
    if put_data:
        new_data = await get_user_data_obj(session, uuid=user_id)
        return new_data
    raise exceptions.user_not_found


@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK,
            dependencies=[Depends(JwtBearer()), Depends(role_check(["admin"]))],
            response_model=bool)
async def delete_user_info(
        user_id: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    delete_data = await delete_user_obj(session, uuid=user_id)
    return delete_data


@router.post("/access", status_code=status.HTTP_200_OK, dependencies=[Depends(JwtBearer())])
@router.post("/refresh", status_code=status.HTTP_200_OK, dependencies=[Depends(JwtBearer())])
async def generate_tokens(
        token: dict = Depends(JwtBearer())
):
    user_id = token["uuid"]
    return JwtBearer.create_tokens(uuid=user_id)


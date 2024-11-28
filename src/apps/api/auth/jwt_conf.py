import time
import logging
from typing import Union

import jwt
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request, HTTPException
import bcrypt

from src.settings import settings

logger = logging.getLogger(__name__)


class JwtBearer(HTTPBearer):
    SECRET_KEY = settings.token.secret_key
    ALGORITHM = settings.token.algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.token.access_token_expire_minutes
    REFRESH_TOKEN_EXPIRE_MINUTES = settings.token.refresh_token_expire_minutes

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise self.credentials_exception

            token_payload = self.verify_access_token(credentials.credentials)
            if not token_payload:
                raise self.credentials_exception

            return token_payload

        raise self.credentials_exception

    @classmethod
    def create_access_token(cls, uuid: str, expires_delta: Union[int, None] = None):
        expire = time.time() + (expires_delta if expires_delta else cls.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        to_encode = {"uuid": uuid, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, uuid: str, expires_delta: Union[int, None] = None):
        expire = time.time() + (expires_delta if expires_delta else cls.REFRESH_TOKEN_EXPIRE_MINUTES * 60)
        to_encode = {"uuid": uuid, "exp": expire, "token_type": "refresh"}
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_access_token(cls, token: str) -> Union[dict, None]:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            return None

    @classmethod
    def verify_refresh_token(cls, token: str) -> Union[dict, None]:
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            if payload.get("token_type") != "refresh":
                return None
            return payload
        except JWTError:
            return None

    @classmethod
    def create_tokens(cls, uuid: str) -> dict:
        access_token = cls.create_access_token(uuid)
        refresh_token = cls.create_refresh_token(uuid)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }


async def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


async def verify_password(password: str, hashed_password: bytes) -> bool:
    pwd_bytes: bytes = password.encode()
    return bcrypt.checkpw(pwd_bytes, hashed_password)

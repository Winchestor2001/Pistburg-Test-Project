import datetime
import re
from typing import Any, Optional, List
from uuid import UUID

from pydantic import BaseModel, validator, Field, ConfigDict


class DefaultDataSchema(BaseModel):
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class UserDataSchema(BaseModel):
    full_name: str
    username: str


class RegistrationUserSchema(UserDataSchema):
    full_name: str
    username: str
    password: str


class ResponseUserSchema(DefaultDataSchema, UserDataSchema):
    is_verified: bool
    role: str

    class Config:
        from_attributes = True


class VerificationUserSchema(BaseModel):
    username: str
    code: str

class AuthenticationUserSchema(BaseModel):
    username: str
    password: str


class PutUserDataSchema(UserDataSchema):
    role: str


class PatchUserDataSchema(BaseModel):
    full_name: str | None = None
    username: str | None = None
    role: str | None = None
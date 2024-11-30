import datetime
from uuid import UUID

from pydantic import BaseModel


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
    role: str


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


class UpdateUserDataSchema(BaseModel):
    full_name: str | None = None
    username: str | None = None
    role: str | None = None
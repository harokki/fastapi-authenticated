from datetime import datetime

from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    username: str
    email: str
    account_name: str
    # TODO: Createには不要
    is_active: bool


class UserAPICreateSchema(UserBaseSchema):
    password: str


class UserCreateSchema(UserAPICreateSchema):
    created_by: str


class UserSchema(UserBaseSchema):
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str

    class Config:
        orm_mode = True


class UserRoleSchema(BaseModel):
    username: str
    role_id: str

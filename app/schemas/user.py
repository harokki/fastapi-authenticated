from datetime import datetime

from pydantic import BaseModel, StrictStr


class UserBaseSchema(BaseModel):
    username: StrictStr
    email: StrictStr
    account_name: StrictStr


class UserAPICreateSchema(UserBaseSchema):
    password: StrictStr


class UserCreateSchema(UserAPICreateSchema):
    is_active: bool
    created_by: str


class UserSchema(UserBaseSchema):
    is_active: bool
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str

    class Config:
        orm_mode = True


class UserRoleSchema(BaseModel):
    username: str
    role_id: str

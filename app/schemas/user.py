import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, constr, validator


class UserBaseSchema(BaseModel):
    # NOTE: constrとmypyの相性が悪い(全てにtype: ignoreしないといけないので微妙)
    #       https://github.com/samuelcolvin/pydantic/issues/156
    username: constr(min_length=1, max_length=32, strict=True)  # type: ignore
    email: constr(min_length=1, max_length=256, strict=True)  # type: ignore
    account_name: constr(min_length=1, max_length=32, strict=True)  # type: ignore

    # NOTE: Fieldのregexはfullmatchが使えなかったり、メッセージが不親切になるのでvalidatorを使う
    @validator("username")
    def validate_username(cls, v):
        if re.compile("[a-zA-Z0-9-_]*").fullmatch(v) is None:
            raise ValueError("only alphanumeric, underscore and hyphen is ok")
        return v

    @validator("email")
    def validate_email(cls, v):
        if re.compile("[a-zA-Z0-9-._]+@[a-zA-Z0-9-._]+.[A-Za-z]+").fullmatch(v) is None:
            raise ValueError("illegal email format")
        return v


class UserAPICreateSchema(UserBaseSchema):
    password: constr(min_length=8, max_length=64, strict=True)  # type: ignore


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


class UserWithRoleSchema(UserBaseSchema):
    is_active: bool
    roles: List[str]
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str


class UserRoleSchema(BaseModel):
    username: str
    role_id: str

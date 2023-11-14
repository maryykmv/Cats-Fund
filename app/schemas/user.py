from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    ...


class UserCreate(schemas.BaseUserCreate):
    ...


class UserUpdate(schemas.BaseUserUpdate):
    ...

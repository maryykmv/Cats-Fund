from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models import User
from app.schemas.user import UserCreate


MESSAGE_INVALID_PASSWORD = 'Password should be at least 3 characters'
MESSAGE_PASSWORD_EXISTS_EMAIL = (
    'Пароль не должен содержать адрес электронной почты')
MESSAGE_USER_REGISTRED = 'Пользователь {} зарегистрирован.'
TOKEN_URL = 'auth/jwt/login'
AUTH_BACKEND_NAME = 'jwt'


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

bearer_transport = BearerTransport(tokenUrl=TOKEN_URL)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name=AUTH_BACKEND_NAME,
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason=MESSAGE_INVALID_PASSWORD
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason=MESSAGE_PASSWORD_EXISTS_EMAIL
            )

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        print(MESSAGE_USER_REGISTRED.format(user.email))


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

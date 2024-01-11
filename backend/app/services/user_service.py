from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Select
from sqlmodel.ext.asyncio.session import AsyncSession

from common import jwt
from common.exception import errors
from common.jwt import superuser_verify
from common.redis import redis_client
from common.response.response_code import CustomCode
from crud.crud_user import UserDao
from database.db_mysql import async_engine
from models.user import User
from schemas.user import Auth2, Avatar, CreateUser, ResetPassword, UpdateUser
from utils.timezone import timezone


class UserService:
    login_time = timezone.now()

    @staticmethod
    async def user_verify(username: str, password: str) -> User:
        async with AsyncSession(async_engine) as db:
            user = await UserDao.get_user_by_username(db, username)
            if not user:
                raise errors.NotFoundError(msg='用户名不存在')
            elif not await jwt.password_verify(password, user.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not user.status:
                raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
            return user

    @staticmethod
    async def login_swagger(*, form_data: OAuth2PasswordRequestForm) -> tuple[str, User]:
        async with AsyncSession(async_engine) as db:
            user = await UserService.user_verify(form_data.username, form_data.password)
            await UserDao.update_user_login_time(db, user.username, login_time=UserService.login_time)
            access_token = await jwt.create_access_token(user.id)
            return access_token, user

    @staticmethod
    async def login_captcha(*, obj: Auth2, request: Request) -> tuple[str, User]:
        async with AsyncSession(async_engine) as db:
            user = await UserService.user_verify(obj.username, obj.password)
            try:
                captcha_code = request.app.state.captcha_uuid
                redis_code = await redis_client.get(f'{captcha_code}')
                if not redis_code:
                    raise errors.ForbiddenError(msg='验证码失效，请重新获取')
            except AttributeError:
                raise errors.ForbiddenError(msg='验证码失效，请重新获取')
            if redis_code.lower() != obj.captcha.lower():
                raise errors.CustomError(error=CustomCode.CAPTCHA_ERROR)
            await UserDao.update_user_login_time(db, user.username, login_time=UserService.login_time)
            access_token = await jwt.create_access_token(user.id)
            return access_token, user

    @staticmethod
    async def register(*, obj: CreateUser) -> None:
        async with AsyncSession(async_engine) as db:
            username = await UserDao.get_user_by_username(db, obj.username)
            if username:
                raise errors.ForbiddenError(msg='该用户名已被注册')
            email = await UserDao.check_email(db, obj.email)
            if email:
                raise errors.ForbiddenError(msg='该邮箱已被注册')
            await UserDao.create_user(db, obj)

    @staticmethod
    async def pwd_reset(*, obj: ResetPassword) -> None:
        async with AsyncSession(async_engine) as db:
            np1 = obj.new_password
            np2 = obj.confirm_password
            if np1 != np2:
                raise errors.ForbiddenError(msg='两次密码输入不一致')
            await UserDao.reset_password(db, obj.username, obj.new_password)

    @staticmethod
    async def get_userinfo(*, username: str) -> User:
        async with AsyncSession(async_engine) as db:
            user = await UserDao.get_user_by_username(db, username=username)
            if not user:
                raise errors.NotFoundError(msg='用户不存在')
            return user

    @staticmethod
    async def update(*, username: str, obj: UpdateUser) -> None:
        async with AsyncSession(async_engine) as db:
            input_user = await UserDao.get_user_by_username(db, username=username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            await superuser_verify(input_user)
            if input_user.username != obj.username:
                _username = await UserDao.get_user_by_username(db, obj.username)
                if _username:
                    raise errors.ForbiddenError(msg='该用户名已存在')
            if input_user.email != obj.email:
                email = await UserDao.check_email(db, obj.email)
                if email:
                    raise errors.ForbiddenError(msg='该邮箱已注册')
            await UserDao.update_userinfo(db, input_user, obj)

    @staticmethod
    async def update_avatar(*, username: str, avatar: Avatar) -> None:
        async with AsyncSession(async_engine) as db:
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            await UserDao.update_avatar(db, input_user, avatar)

    @staticmethod
    async def get_select(*, username: str = None, phone: str = None, status: int = None) -> Select:
        return await UserDao.get_all(username=username, phone=phone, status=status)

    @staticmethod
    async def update_permission(*, current_user: User, pk: int) -> None:
        async with AsyncSession(async_engine) as db:
            await superuser_verify(current_user)
            if not await UserDao.get_user_by_id(db, pk):
                raise errors.NotFoundError(msg='用户不存在')
            else:
                if pk == current_user.id:
                    raise errors.ForbiddenError(msg='禁止修改自身管理员权限')
                await UserDao.super_set(db, pk)

    @staticmethod
    async def update_status(*, current_user: User, pk: int) -> None:
        async with AsyncSession(async_engine) as db:
            await superuser_verify(current_user)
            if not await UserDao.get(db, pk):
                raise errors.NotFoundError(msg='用户不存在')
            else:
                if pk == current_user.id:
                    raise errors.ForbiddenError(msg='禁止修改自身状态')
                await UserDao.status_set(db, pk)

    @staticmethod
    async def delete(*, current_user: User, username: str) -> None:
        async with AsyncSession(async_engine) as db:
            await superuser_verify(current_user)
            input_user = await UserDao.get_user_by_username(db, username)
            if not input_user:
                raise errors.NotFoundError(msg='用户不存在')
            await UserDao.delete_user(db, input_user.id)

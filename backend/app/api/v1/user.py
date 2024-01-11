from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from common.jwt import CurrentUser, DependsJwtUser
from common.pagination import PageDepends, paging_data
from common.response.response_schema import response_base
from database.db_mysql import async_engine
from schemas.user import Avatar, CreateUser, GetUserInfo, ResetPassword, UpdateUser
from services.user_service import UserService

router = APIRouter()


@router.post('/register', summary='사용자 등록')
async def user_register(obj: CreateUser):
    await UserService.register(obj=obj)
    return await response_base.success()


@router.post('/password/reset', summary='비밀번호 재설정', dependencies=[DependsJwtUser])
async def password_reset(obj: ResetPassword):
    await UserService.pwd_reset(obj=obj)
    return await response_base.success()


@router.get('/{username}', summary='사용자 정보 보기', dependencies=[DependsJwtUser])
async def get_user(username: str):
    data = await UserService.get_userinfo(username=username)
    return await response_base.success(data=data)


@router.put('/{username}', summary='사용자 정보 업데이트', dependencies=[DependsJwtUser])
async def update_userinfo(username: str, obj: UpdateUser):
    await UserService.update(username=username, obj=obj)
    return await response_base.success()


@router.put('/{username}/avatar', summary='아바타 업데이트', dependencies=[DependsJwtUser])
async def update_avatar(username: str, avatar: Avatar):
    await UserService.update_avatar(username=username, avatar=avatar)
    return await response_base.success()


@router.get(
    '', summary='(퍼지 조건) 모든 사용자를 불러오기 위한 페이징 호출', dependencies=[DependsJwtUser, PageDepends]
)
async def get_all_users(
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    async with AsyncSession(async_engine) as db:
        user_select = await UserService.get_select(username=username, phone=phone, status=status)
        page_data = await paging_data(db, user_select, GetUserInfo)
    return await response_base.success(data=page_data)


@router.put('/{pk}/super', summary='사용자 슈퍼 권한 수정', dependencies=[DependsJwtUser])
async def super_set(current_user: CurrentUser, pk: int):
    await UserService.update_permission(current_user=current_user, pk=pk)
    return await response_base.success()


@router.put('/{pk}/status', summary='사용자 상태 수정하기', dependencies=[DependsJwtUser])
async def status_set(current_user: CurrentUser, pk: int):
    await UserService.update_status(current_user=current_user, pk=pk)
    return await response_base.success()


@router.delete(
    path='/{username}',
    summary='사용자 삭제',
    description='사용자 로그아웃! = 사용자가 로그아웃되었음을 의미하며, '
    '로그아웃 후 데이터베이스에서 사용자가 삭제됩니다.',
    dependencies=[DependsJwtUser],
)
async def delete_user(current_user: CurrentUser, username: str):
    await UserService.delete(current_user=current_user, username=username)
    return await response_base.success()

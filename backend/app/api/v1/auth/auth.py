
from common.jwt import DependsJwtUser
from common.response.response_schema import response_base
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import Token
from schemas.user import Auth2
from services.user_service import UserService

router = APIRouter()


@router.post('/swagger_login', summary='swagger 양식 로그인', description='form 로그인 형식 지정, 다음 경우에만 해당 swagger 문서 디버깅 인터페이스')
async def swagger_user_login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    token, user = await UserService.login_swagger(form_data=form_data)
    return Token(access_token=token, user=user)  # type: ignore


@router.post('/login', summary='캡차 로그인')
async def user_login(request: Request, obj: Auth2) -> Token:
    token, user = await UserService.login_captcha(obj=obj, request=request)
    return Token(access_token=token, user=user)  # type: ignore


@router.post('/logout', summary='로그아웃', dependencies=[DependsJwtUser])
async def user_logout():
    return await response_base.success()

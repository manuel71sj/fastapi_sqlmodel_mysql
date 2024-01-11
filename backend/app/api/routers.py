
from fastapi import APIRouter

from api.v1.auth import router as auth_router
from api.v1.user import router as user_router
from core.conf import settings

v1 = APIRouter(prefix=settings.API_V1_STR)

v1.include_router(auth_router, prefix='/auth', tags=['인증'])

v1.include_router(user_router, prefix='/users', tags=['사용자'])

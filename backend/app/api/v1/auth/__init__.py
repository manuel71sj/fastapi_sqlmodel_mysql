
from fastapi import APIRouter

from api.v1.auth.auth import router as auth_router
from api.v1.auth.captcha import router as captcha_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(captcha_router)

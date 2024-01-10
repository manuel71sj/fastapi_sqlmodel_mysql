
from common.redis import redis_client
from core.conf import settings
from fast_captcha import img_captcha
from fastapi import APIRouter, Depends, Request
from fastapi_limiter.depends import RateLimiter
from starlette.concurrency import run_in_threadpool
from starlette.responses import StreamingResponse
from utils.generate_string import get_uuid4_str

router = APIRouter()


@router.get('/captcha', summary='캡차 받기', dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def get_captcha(request: Request):
    img, code = await run_in_threadpool(img_captcha)
    uuid = get_uuid4_str()
    request.app.state.captcha_uuid = uuid
    await redis_client.set(uuid, code, settings.CAPTCHA_EXPIRATION_TIME)
    return StreamingResponse(content=img, media_type='image/jpeg')

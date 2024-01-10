
from contextlib import asynccontextmanager

from api.routers import v1
from common.exception.exception_handler import register_exception
from common.redis import redis_client
from core.conf import settings
from database.db_mysql import create_table
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from middleware.access_middle import AccessMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from utils.health_check import ensure_unique_route_names, http_limit_callback


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    초기화 시작

    :return:
    """
    # 데이터베이스 테이블 만들기
    await create_table()
    # redis 연결
    await redis_client.open()
    # 리미터 초기화
    await FastAPILimiter.init(redis_client, prefix=settings.LIMITER_REDIS_PREFIX, http_callback=http_limit_callback)

    yield

    # redis 연결 닫기
    await redis_client.close()
    # 닫기 리미터
    await FastAPILimiter.close()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=register_init,
    )

    # 정적 파일
    register_static_file(app)

    # 미들웨어
    register_middleware(app)

    # 라우팅(컴퓨터 네트워크에서)
    register_router(app)

    # 분페이지
    register_page(app)

    # 글로벌 예외 처리
    register_exception(app)

    return app


def register_static_file(app: FastAPI):
    """
    정적 파일 상호 작용 개발 모델, nginx 정적 리소스 서비스를 사용한 프로덕션

    :param app:
    :return:
    """
    if settings.STATIC_FILE:
        import os

        from fastapi.staticfiles import StaticFiles

        if not os.path.exists('./static'):
            os.mkdir('./static')
        app.mount('/static', StaticFiles(directory='static'), name='static')


def register_middleware(app) -> None:
    # gzip
    if settings.MIDDLEWARE_GZIP:
        app.add_middleware(GZipMiddleware)
    # 인터페이스 액세스 로그
    if settings.MIDDLEWARE_ACCESS:
        app.add_middleware(AccessMiddleware)
    # 교차 도메인
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    """
    路由

    :param app: FastAPI
    :return:
    """
    app.include_router(v1)

    # Extra
    ensure_unique_route_names(app)


def register_page(app: FastAPI):
    """
    分页查询

    :param app:
    :return:
    """
    add_pagination(app)

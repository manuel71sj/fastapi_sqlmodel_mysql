import sys

from redis.asyncio.client import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from common.log import log
from core.conf import settings


class RedisCli(Redis):
    def __init__(self):
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            # db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,  # 트랜스코딩 utf-8
            ssl=True,
        )

    async def open(self):
        """
        초기화 연결 트리거

        :return:
        """
        try:
            await self.ping()
        except TimeoutError:
            log.error('❌ REDIS 연결 시간 초과')
            sys.exit()
        except AuthenticationError:
            log.error('❌ REDIS 연결 인증 실패')
            sys.exit()
        except Exception as e:
            log.error('❌ REDIS 연결 이상 {}', e)
            sys.exit()


# 创建redis连接对象
redis_client = RedisCli()

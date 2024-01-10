
from datetime import datetime

from sqlmodel import Field
from utils.timezone import timezone

id_key = Field(exclude=True, primary_key=True, description='主键id')

""" warning
❓ MiXin 지원하지 않는 것 같습니다.：https://github.com/tiangolo/sqlmodel/pull/256
"""


# Mixin: 구조를 더 명확하게 만드는 객체 지향 프로그래밍 개념, `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin:
    """用户 Mixin 数据类"""

    create_user: int = Field(description='创建者')
    update_user: int | None = Field(exclude=True, default=None, description='修改者')


class DateTimeMixin:
    """日期时间 Mixin 数据类"""

    created_time: datetime = Field(
        exclude=True, sa_column_kwargs={'default_factory': timezone.now}, description='创建时间'
    )
    updated_time: datetime | None = Field(
        exclude=True, sa_column_kwargs={'onupdate': timezone.now}, description='更新时间'
    )

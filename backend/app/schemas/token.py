

from schemas.base import SchemaBase
from schemas.user import GetUserInfo


class Token(SchemaBase):
    code: int = 200
    msg: str = 'Success'
    access_token: str
    token_type: str = 'Bearer'
    user: GetUserInfo

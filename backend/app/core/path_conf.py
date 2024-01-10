
import os

from pathlib import Path

# 프로젝트 루트 디렉터리 가져오기
# 또는 백엔드 디렉토리의 절대 경로를 사용하세요.windows：BasePath = D:\git_project\fastapi_mysql\backend
BasePath = Path(__file__).resolve().parent.parent.parent


# 마이그레이션 파일 저장 경로
Versions = os.path.join(BasePath, 'app', 'alembic', 'versions')

# 로그 파일 경로
LogPath = os.path.join(BasePath, 'app', 'log')

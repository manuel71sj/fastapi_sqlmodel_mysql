# FastAPI SQLModel Architecture

파이썬 3.10을 기반으로 하는 FastAPI 프레임워크의 기본 프로젝트로 개발되었습니다.

## 진단 속성

- [x] FastAPI > 0.100.0
- [x] Async design
- [x] Restful API
- [x] SQLAlchemy 2.0
- [x] Pydantic 2.0
- [ ] ......

## TODO

- [ ] Docker

## 활용

> [!WARNING]
> 이 과정에서 특히 8000, 3306, 6379...와 같은 포트가 점유하는 것에 특히 주의하세요.

### 1: 레거시

1. 종속성 설치

    ```shell
    pip install -r requirements.txt
    ```

2. 데이터베이스 `fsm`을 생성하고, 인코딩을 utf8mb4로 선택합니다.
3. redis를 설치하고 시작합니다.
4. `backend/app/` 디렉터리에 `.env` 파일을 생성합니다.

    ```shell
    cd backend/app/
    touch .env
    ```

5. .env.example`를 `.env`에 복사합니다.

   ```shell
   cp .env.example .env
   ```

6. 데이터베이스 마이그레이션 [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

    ```shell
    cd backend/app/
    
    # 마이그레이션 파일 생성
    alembic revision --autogenerate
    
    # 구현 마이그레이션
    alembic upgrade head
    ```

7. 백엔드/앱/main.py 파일을 실행하여 서비스를 시작합니다.
8. 브라우저 액세스: http://127.0.0.1:8000/api/v1/docs

---

### 2: docker

[TODO](#TODO)

## 상호 작용

현재 채널은 하나뿐이므로 진위 여부 확인에 주의하세요.

<table>
  <tr>
    <td><a href="https://t.me/+ZlPhIFkPp7E4NGI1">직접 링크 점프</a></td>
  </tr>
  <tr>
    <td> Telegram </td>
  </tr>
</table>

## 스폰서십

이 프로젝트가 도움이 된다면 저자에게 커피 원두를 후원하여 격려를 표시할 수 있습니다: 커피:.

<table>
  <tr>
    <td><img src="https://github.com/wu-clan/image/blob/master/pay/weixin.jpg?raw=true" width="180px" alt="Wechat"/>
    <td><img src="https://github.com/wu-clan/image/blob/master/pay/zfb.jpg?raw=true" width="180px" alt="Alipay"/>
    <td><img src="https://github.com/wu-clan/image/blob/master/pay/ERC20.jpg?raw=true" width="180px" alt="0x40D5e2304b452256afD9CE2d3d5531dc8d293138"/>
  </tr>
  <tr>
    <td align="center">마이크로 소프트</td>
    <td align="center">알리페이, 온라인 결제 플랫폼</td>
    <td align="center">ERC20</td>
  </tr>
</table>

## 라이선스

본 프로젝트는 MIT 라이선스 조건에 따라 라이선스가 부여됩니다.

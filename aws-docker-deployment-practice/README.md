# AWS Docker Pull 배포 실습

로컬에서 FastAPI Backend와 Streamlit Frontend 이미지를 만든 뒤 Docker Hub에 올리고,
Ubuntu EC2에서 Redis·PostgreSQL과 연결하여 실행하는 실습입니다.

## 구성

```text
backend/              FastAPI 소스와 Dockerfile
frontend/             Streamlit 소스와 Dockerfile
database/init.sql     PostgreSQL 초기 Schema
compose.yml           로컬 Build용 Compose
compose.release.yml   Docker Hub Pull 배포용 Compose
.env.example          환경변수 예시(Secret 없음)
docs/                 단계별 실습 기록
```

실제 `.env`, PEM 키, `.venv`는 공유하거나 Git에 올리지 않습니다.

## 전체 순서

처음부터 끝까지 한 파일만 보며 실습하려면
[`00_처음부터_끝까지_실행가이드.md`](./00_처음부터_끝까지_실행가이드.md)를 사용합니다.
아래 `docs/` 문서는 단계별 개념을 다시 확인할 때 사용합니다.

1. `docs/01-architecture.md`로 구조를 확인합니다.
2. `docs/02-local-build-and-push.md`로 이미지를 Docker Hub에 올립니다.
3. `docs/03-create-ec2.md`로 EC2와 보안 그룹을 준비합니다.
4. `docs/04-install-infrastructure.md`로 Docker·Redis·PostgreSQL·Schema를 준비합니다.
5. `docs/05-transfer-and-deploy.md`로 배포 파일을 전송하고 실행합니다.
6. `docs/06-verification.md`로 상태와 로그를 확인합니다.
7. 실습 종료 시 `docs/07-cleanup.md`를 확인합니다.

## 빠른 로컬 Build

```powershell
Copy-Item .env.example .env
docker compose config --quiet
docker compose build backend frontend
```

`.env`에 실제 Key를 넣었다면 화면 공유나 제출 전에 반드시 제외합니다.

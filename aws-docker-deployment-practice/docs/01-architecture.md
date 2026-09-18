# 01 아키텍처

```text
Windows 개발 PC
  ├─ Backend Image Build ─┐
  └─ Frontend Image Build ├─> Docker Hub
                          │
AWS EC2 Ubuntu <──────────┘ Pull
  ├─ Backend :8000
  ├─ Frontend :8501
  ├─ Redis :6379 (외부 비공개)
  └─ PostgreSQL :5432 (외부 비공개)
```

개발자는 Backend·Frontend 이미지만 Docker Hub에 올립니다. Redis와 PostgreSQL은 공식
이미지를 EC2가 직접 받습니다. `.env`는 실행 시 환경변수를 전달하며 이미지에 포함하지
않습니다. `.venv`도 Docker 이미지에 넣지 않고 `requirements.txt`로 패키지를 설치합니다.


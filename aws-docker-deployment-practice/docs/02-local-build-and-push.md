# 02 로컬 Build와 Docker Hub Push

프로젝트 최상위에서 실행합니다.

```powershell
docker compose config --quiet
docker compose build backend frontend
docker image ls
```

Docker Hub용 태그를 붙이고 Push합니다.

```powershell
docker tag simple-multi-llm-app-backend:latest hyunport/simple-multi-llm-backend:1.0.0
docker tag simple-multi-llm-app-frontend:latest hyunport/simple-multi-llm-frontend:1.0.0
docker login
docker push hyunport/simple-multi-llm-backend:1.0.0
docker push hyunport/simple-multi-llm-frontend:1.0.0
```

Push 결과에 `digest: sha256:...`가 나오면 완료입니다.


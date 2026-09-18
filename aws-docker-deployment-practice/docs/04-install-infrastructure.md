# 04 Docker와 인프라 준비

Ubuntu에서 Docker와 Compose를 설치합니다.

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-v2 git curl
sudo systemctl enable --now docker
sudo usermod -aG docker ubuntu
exit
```

재접속 후 확인합니다.

```bash
docker info
docker compose version
```

수업자료의 `05_llm-agent-orchestration/00_local-runtime` 명령을 참고하여 Redis와
PostgreSQL을 실행합니다. 실행 후 다음처럼 확인합니다. 컨테이너 이름은 실제 이름에
맞춥니다.

```bash
docker ps
docker exec aidevs-redis redis-cli ping
docker exec aidevs-pgvector pg_isready -U agent_user -d agent_db
```

`database/init.sql`의 SQL을 PostgreSQL에 적용하고 `\dt`로 테이블을 확인합니다.


# 06 배포 검증

EC2 내부에서 확인합니다.

```bash
curl --fail http://127.0.0.1:8000/health/ready
curl -I http://127.0.0.1:8501
docker compose -f compose.release.yml ps
```

로컬 브라우저에서는 다음 주소를 확인합니다.

```text
http://<PUBLIC_IP>:8501
http://<PUBLIC_IP>:8000/health/ready
```

오류가 나면 삭제하기 전에 로그를 확인합니다.

```bash
docker compose -f compose.release.yml logs --tail=100 backend
docker compose -f compose.release.yml logs --tail=100 frontend
```


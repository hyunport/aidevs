# 07 종료와 정리

애플리케이션만 종료합니다.

```bash
cd ~/test
docker compose -f compose.release.yml down
```

Redis·PostgreSQL과 데이터 Volume은 별도 확인 없이 삭제하지 않습니다. 실습 종료 후에는
AWS 비용 방지를 위해 EC2 인스턴스와 연결된 EBS·Elastic IP 등 남은 자원을 AWS Console에서
확인합니다. 삭제 전 필요한 데이터와 정확한 대상을 먼저 확인합니다.


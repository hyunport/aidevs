# 05 파일 전송과 배포

로컬에서 `.env.example`을 복사해 실제 `.env`를 만들고 Key·DB 비밀번호·이미지 이름을
설정합니다. `.env`와 `compose.release.yml`만 EC2에 보냅니다.

```powershell
scp -i ".\Agentkey.pem" ".\.env" ".\compose.release.yml" ubuntu@<PUBLIC_IP>:~/test/
```

EC2에서 Secret 파일 권한을 제한하고 배포합니다.

```bash
cd ~/test
chmod 600 .env
docker login
docker compose -f compose.release.yml config --quiet
docker compose -f compose.release.yml pull
docker compose -f compose.release.yml up -d
docker compose -f compose.release.yml ps
```

로그인과 Compose는 같은 사용자 권한으로 실행합니다. Docker 그룹 권한이 정상이라면
`sudo` 없이 실행합니다.


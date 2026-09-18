# 03 EC2 생성과 SSH 접속

Ubuntu EC2를 만들고 기존 PEM 키를 선택합니다. 보안 그룹의 **인바운드 규칙 편집**에서
다음 규칙을 설정합니다.

| 유형 | 프로토콜 | 포트 | Source |
| --- | --- | ---: | --- |
| SSH | TCP | 22 | 내 IP (`공인 IP/32`) |
| 사용자 지정 TCP | TCP | 8000 | 내 IP (`공인 IP/32`) |
| 사용자 지정 TCP | TCP | 8501 | 내 IP (`공인 IP/32`) |

Redis `6379`와 PostgreSQL `5432`는 외부에 공개하지 않습니다. 아웃바운드는 패키지 설치,
Docker Hub Pull, 외부 API 호출을 위해 기본 `모든 트래픽 / 0.0.0.0/0` 규칙을 유지합니다.
아웃바운드 화면에 SSH·8000·8501 규칙을 입력하지 않습니다.

로컬 PowerShell에서 접속합니다.

```powershell
ssh -i "C:\path\Agentkey.pem" ubuntu@<PUBLIC_IP>
```

Private IP가 아닌 EC2의 Public IPv4 또는 Public DNS를 사용합니다.

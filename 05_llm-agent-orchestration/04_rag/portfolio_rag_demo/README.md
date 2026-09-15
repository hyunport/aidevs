# 포트폴리오 RAG 데모

실제 Markdown 문서를 pgvector에 색인하고 Ollama가 검색 문서만 근거로 답하는 교육용 예제다.

## 구성

- 사용자: 태웅님(성장형), 오현님(균형형), 기화님(안정형)
- 전용 pgvector: `portfolio-pgvector`, 호스트 포트 `5434`
- 공용 Ollama: `127.0.0.1:11434`
- 공용 Redis: `127.0.0.1:6379`
- 컬렉션: `portfolio_demo`

## 1. 전용 pgvector 시작

```powershell
.\start-portfolio-pgvector.ps1
```

## 2. Markdown 문서 색인 및 검색 확인

첫 실행 시 필요한 DB Schema도 자동 생성한다.

```powershell
python .\01_index_portfolios.py
```

## 3. RAG 답변 생성

기본 질문을 실행한다.

```powershell
python .\02_portfolio_rag_answer.py
```

원하는 질문을 명령행으로 전달할 수도 있다.

```powershell
python .\02_portfolio_rag_answer.py "태웅님과 기화님의 투자 위험도를 비교해줘."
```

## 4. Redis 캐시 확인

```powershell
python .\03_portfolio_rag_cache.py
```

첫 질문은 Redis MISS로 RAG를 실행하고, 두 번째 동일 질문은 Redis HIT로 저장된 답변을 반환한다.

## 추천 질문

- 태웅님의 포트폴리오와 주요 위험을 분석해줘.
- 오현님의 포트폴리오는 균형적으로 구성되어 있어?
- 기화님의 자산별 현재 투자 금액을 계산해줘.
- 태웅님과 기화님의 투자 위험도를 비교해줘.
- 태웅님이 균형형으로 변경하려면 얼마씩 매수하거나 매도해야 해?

## 주의

이 프로젝트는 교육용 데모다. 실제 투자 권유나 투자 자문을 제공하지 않는다.


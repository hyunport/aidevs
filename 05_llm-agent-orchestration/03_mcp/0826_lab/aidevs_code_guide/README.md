# AIDEVS 코드 길잡이 Agent

`aidevs` 전체의 `README.md`를 OpenAI Embedding으로 pgvector에 색인하고, 자연어
요청과 관련된 수업 자료 여러 개 및 각 자료 주변의 최신 코드 파일을 추천합니다.

## 구성

```text
사용자 질문
→ GPT Agent가 search_readmes MCP Tool 선택
→ 질문을 text-embedding-3-small로 변환
→ 로컬 PostgreSQL/pgvector에서 README Chunk 검색
→ README 중복 제거 후 최대 5개 선택
→ 같은 폴더와 바로 아래 폴더의 최신 코드 파일 목록 추가
→ GPT가 파일 경로와 학습 순서를 설명
```

README만 임베딩하므로 코드가 변경되어도 재색인이 필요하지 않습니다. 코드 파일 목록은
검색 시점에 다시 읽습니다. README가 변경되면 `index_readmes.py`를 다시 실행하며,
내용 Hash가 달라진 Chunk만 OpenAI API로 다시 임베딩합니다.

## 사전 준비

상위 `05_llm-agent-orchestration/.env`에 다음 값이 필요합니다.

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4.1-mini
DATABASE_URL=postgresql://agent_user:agent_password@127.0.0.1:5433/agent_db

# 선택 사항
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_EMBEDDING_DIMENSIONS=1536
README_CHUNK_SIZE=2400
README_CHUNK_OVERLAP=240
```

`.env`는 Git에 올리지 않습니다.

## 실행

```powershell
cd C:\Port_수업자료\aidevs\05_llm-agent-orchestration

# 1. API 호출 없이 색인 대상과 변경량 확인
.\.venv\Scripts\python.exe .\03_mcp\0826_lab\aidevs_code_guide\index_readmes.py --dry-run

# 2. 최초 README 색인 또는 변경분 갱신
.\.venv\Scripts\python.exe .\03_mcp\0826_lab\aidevs_code_guide\index_readmes.py

# 3. Agent 실행
.\.venv\Scripts\python.exe .\03_mcp\0826_lab\aidevs_code_guide\agent.py "로그인 가능한 여행 추천 서비스를 만들고 싶어"

# MCP Tool만 빠르게 점검
.\.venv\Scripts\python.exe .\03_mcp\0826_lab\aidevs_code_guide\smoke_test.py

# Tool 호출 과정까지 확인
.\.venv\Scripts\python.exe .\03_mcp\0826_lab\aidevs_code_guide\agent.py "RAG 관련 코드를 찾아줘" --trace
```

## 테스트

```powershell
cd C:\Port_수업자료\aidevs\05_llm-agent-orchestration\03_mcp\0826_lab\aidevs_code_guide
..\..\..\.venv\Scripts\python.exe -m pytest .\tests -q
```

## 검색 Tool

Agent에 공개되는 Tool은 하나입니다.

```python
search_readmes(query: str, top_k: int = 5)
```

결과에는 README 경로, 유사도, 일치한 Chunk 일부, 같은 폴더와 바로 아래 폴더의
코드 파일 목록이 포함됩니다. `top_k`는 1~10 범위로 제한됩니다.

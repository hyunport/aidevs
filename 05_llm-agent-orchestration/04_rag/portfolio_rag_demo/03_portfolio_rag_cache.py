"""같은 포트폴리오 질문의 답변을 Redis에서 재사용합니다."""

from _ollama_env import load_local_env

load_local_env()

from _portfolio_rag import CHAT_MODEL, answer_question
from _pgvector_store import EMBEDDING_MODEL
from _redis_cache import JsonCache, cache_key


CACHE_NAMESPACE = "portfolio-rag-answer:v1"
PORTFOLIO_VERSION = "2026-08-31-v1"
QUESTION = "태웅님의 포트폴리오를 분석하고 주요 위험을 알려줘."


def ask(question: str, cache: JsonCache) -> dict:
    key = cache_key(
        CACHE_NAMESPACE,
        {
            "question": question,
            "embedding_model": EMBEDDING_MODEL,
            "chat_model": CHAT_MODEL,
            "portfolio_version": PORTFOLIO_VERSION,
        },
    )
    cached = cache.get(key)
    if cached:
        return {**cached, "cache_hit": True, "ttl": cache.ttl(key)}

    result = answer_question(question)
    saved = cache.set(key, result)
    return {**result, "cache_hit": False, "cache_saved": saved}


if __name__ == "__main__":
    redis_cache = JsonCache()
    redis_cache.delete_namespace(CACHE_NAMESPACE)

    first = ask(QUESTION, redis_cache)
    print("1차 질문: Redis MISS → RAG 실행")
    print(first)

    second = ask(QUESTION, redis_cache)
    if second["cache_hit"]:
        print("\n2차 동일 질문: Redis HIT → 저장된 답변 반환")
    else:
        print("\n2차 동일 질문: Redis 저장 실패 → RAG 다시 실행")
    print(second)


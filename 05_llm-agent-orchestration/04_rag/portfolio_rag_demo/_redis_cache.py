"""포트폴리오 RAG 답변을 위한 Redis JSON Cache."""

import hashlib
import json
import os
from typing import Any

import redis


REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
DEFAULT_TTL_SECONDS = int(os.getenv("REDIS_TTL_SECONDS", "1800"))


def cache_key(namespace: str, payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"rag:{namespace}:{digest}"


class JsonCache:
    def __init__(self, url: str = REDIS_URL) -> None:
        self.client = redis.from_url(url, decode_responses=True, socket_connect_timeout=2)

    def get(self, key: str) -> dict[str, Any] | None:
        try:
            value = self.client.get(key)
            if value is None:
                return None
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else None
        except (redis.RedisError, json.JSONDecodeError):
            return None

    def set(self, key: str, value: dict[str, Any], *, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> bool:
        if ttl_seconds < 1:
            raise ValueError("ttl_seconds는 1 이상이어야 합니다.")
        try:
            self.client.setex(key, ttl_seconds, json.dumps(value, ensure_ascii=False))
            return True
        except redis.RedisError:
            return False

    def ttl(self, key: str) -> int | None:
        try:
            value = self.client.ttl(key)
            return value if value >= 0 else None
        except redis.RedisError:
            return None

    def delete_namespace(self, namespace: str) -> int | None:
        pattern = f"rag:{namespace}:*"
        try:
            keys = list(self.client.scan_iter(match=pattern, count=100))
            return self.client.delete(*keys) if keys else 0
        except redis.RedisError:
            return None

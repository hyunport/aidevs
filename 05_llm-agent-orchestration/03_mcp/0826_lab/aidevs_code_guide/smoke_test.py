"""GPT 답변 생성 없이 MCP Tool 연결과 실행만 확인합니다."""

import asyncio
import json

from openai import AsyncOpenAI

from config import get_settings
from stdio_client import connect_to_guide_server


async def main() -> None:
    settings = get_settings()
    query = "RAG 관련 수업 자료와 코드를 찾아줘"
    async with AsyncOpenAI(api_key=settings.openai_api_key) as client:
        response = await client.embeddings.create(
            model=settings.embedding_model,
            input=query,
            dimensions=settings.embedding_dimensions,
        )
    query_embedding = response.data[0].embedding

    async with connect_to_guide_server() as session:
        tools = (await asyncio.wait_for(session.list_tools(), timeout=10)).tools
        print("tools:", [tool.name for tool in tools])
        result = await asyncio.wait_for(
            session.call_tool(
                "search_readmes",
                {
                    "query": query,
                    "query_embedding": query_embedding,
                    "top_k": 3,
                },
            ),
            timeout=60,
        )
        texts = [content.text for content in result.content if hasattr(content, "text")]
        payload = json.loads("\n".join(texts))
        print("is_error:", bool(result.isError))
        print("result_count:", len(payload.get("results", [])))
        for item in payload.get("results", []):
            print("-", item["readme_path"])


if __name__ == "__main__":
    asyncio.run(main())

"""GPT가 search_readmes MCP Tool을 사용해 수업 자료를 추천합니다."""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

from openai import AsyncOpenAI

from config import get_settings
from stdio_client import connect_to_guide_server


INSTRUCTIONS = """
당신은 AIDEVS 수업 코드 길잡이입니다.
사용자가 프로젝트 아이디어나 필요한 기능을 말하면 반드시 search_readmes Tool을 호출하세요.
검색된 자료가 여러 개면 기능별로 분류하고, README 경로와 관련 코드 파일을 정확히 표시하세요.
Tool 결과에 없는 파일이나 내용을 만들어내지 마세요.
마지막에는 추천 학습 순서를 짧게 제시하세요.
""".strip()


def to_openai_tool(tool) -> dict[str, Any]:
    raw = tool.model_dump(by_alias=True)
    parameters = raw["inputSchema"]
    # query_embedding은 Backend가 OpenAI Embedding API로 생성하는 내부 인자입니다.
    # LLM에는 사용자가 제공할 수 있는 query와 top_k만 공개합니다.
    parameters.get("properties", {}).pop("query_embedding", None)
    if "required" in parameters:
        parameters["required"] = [
            name for name in parameters["required"] if name != "query_embedding"
        ]
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": parameters,
        "strict": False,
    }


def text_result(result) -> str:
    return "\n".join(
        content.text for content in result.content if hasattr(content, "text")
    )


async def answer(question: str) -> dict[str, Any]:
    settings = get_settings()
    trace: list[dict[str, Any]] = []

    async with AsyncOpenAI(api_key=settings.openai_api_key) as client:
        async with connect_to_guide_server() as session:
            discovered = (await session.list_tools()).tools
            available = {tool.name for tool in discovered}
            response = await client.responses.create(
                model=settings.openai_model,
                instructions=INSTRUCTIONS,
                input=question,
                tools=[to_openai_tool(tool) for tool in discovered],
                tool_choice="required",
            )
            tool_calls = [
                item for item in response.output if item.type == "function_call"
            ]
            if not tool_calls:
                raise RuntimeError("Agent가 search_readmes Tool을 선택하지 않았습니다.")

            outputs = []
            for call in tool_calls:
                if call.name not in available:
                    raise ValueError(f"허용되지 않은 Tool입니다: {call.name}")
                arguments = json.loads(call.arguments)
                if not isinstance(arguments, dict):
                    raise ValueError("Tool arguments는 JSON Object여야 합니다.")
                trace_arguments = dict(arguments)
                if call.name == "search_readmes":
                    query = str(arguments.get("query", "")).strip()
                    embedding_response = await client.embeddings.create(
                        model=settings.embedding_model,
                        input=query,
                        dimensions=settings.embedding_dimensions,
                    )
                    arguments["query_embedding"] = embedding_response.data[0].embedding
                result = await session.call_tool(call.name, arguments)
                result_text = text_result(result)
                trace.append(
                    {
                        "tool": call.name,
                        "arguments": trace_arguments,
                        "is_error": bool(result.isError),
                        "result": result_text,
                    }
                )
                outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": result_text,
                    }
                )

            final_response = await client.responses.create(
                model=settings.openai_model,
                instructions=INSTRUCTIONS,
                previous_response_id=response.id,
                input=outputs,
            )
            return {
                "question": question,
                "model": settings.openai_model,
                "tools": sorted(available),
                "trace": trace,
                "answer": final_response.output_text,
            }


async def main() -> None:
    parser = argparse.ArgumentParser(description="AIDEVS 코드 길잡이 Agent")
    parser.add_argument(
        "question",
        nargs="?",
        default="로그인 가능한 여행 추천 서비스를 만들고 싶어.",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="최종 답변뿐 아니라 Tool 호출 과정도 출력합니다.",
    )
    args = parser.parse_args()
    result = await answer(args.question)
    if args.trace:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["answer"])


if __name__ == "__main__":
    asyncio.run(main())

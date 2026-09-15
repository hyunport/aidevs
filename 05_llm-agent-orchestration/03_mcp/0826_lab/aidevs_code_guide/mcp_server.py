"""AIDEVS README 검색 Tool 하나를 제공하는 stdio MCP Server입니다."""

from mcp.server.fastmcp import FastMCP

from search_service import search_readmes as run_search


mcp = FastMCP(
    "aidevs-code-guide",
    instructions=(
        "AIDEVS 수업 README를 의미 검색하고 관련된 최신 코드 파일 목록을 제공합니다."
    ),
)


@mcp.tool()
def search_readmes(
    query: str,
    query_embedding: list[float],
    top_k: int = 5,
) -> dict:
    """자연어 질문과 관련된 README 여러 개 및 주변 코드 파일을 검색합니다."""
    return run_search(
        query=query,
        query_embedding=query_embedding,
        top_k=top_k,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")

"""부산과 서울의 관광지 정보를 제공하는 교육용 stdio MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "tour",
    instructions="부산과 서울의 주요 관광지 정보를 제공합니다.",
)


TOURIST_ATTRACTIONS = {
    "부산": [
        {
            "name": "해운대해수욕장",
            "description": "부산을 대표하는 해변 관광지입니다.",
        },
        {
            "name": "감천문화마을",
            "description": "형형색색의 건물과 골목 풍경으로 유명한 마을입니다.",
        },
    ],
    "서울": [
        {
            "name": "경복궁",
            "description": "조선 시대의 대표적인 궁궐입니다.",
        },
        {
            "name": "남산서울타워",
            "description": "서울 도심을 한눈에 볼 수 있는 전망 명소입니다.",
        },
    ],
}


@mcp.tool()
def get_tourist_attractions(city: Literal["부산", "서울"]) -> dict:
    """도시의 주요 관광지 정보를 조회합니다."""
    return {
        "city": city,
        "items": TOURIST_ATTRACTIONS[city],
        "source": "lab-tour-service",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
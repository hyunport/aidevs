"""AIDEVS 검색 MCP Server와 stdio로 연결합니다."""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = Path(__file__).with_name("mcp_server.py")


@asynccontextmanager
async def connect_to_guide_server():
    parameters = StdioServerParameters(command=sys.executable, args=[str(SERVER_PATH)])
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session

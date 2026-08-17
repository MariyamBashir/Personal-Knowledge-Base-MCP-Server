import asyncio
import sys

from fastmcp import Client
from fastmcp.client.transports import StdioTransport


async def main():

    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "app.mcp_server"],
    )

    async with Client(transport) as client:

        print("=== AVAILABLE TOOLS ===")

        tools = await client.list_tools()

        for tool in tools:
            print(f"- {tool.name}")

        print()

        print("=== PING ===")

        ping_result = await client.call_tool(
            "ping",
            {},
        )

        print(ping_result)

        print()

        print("=== SEARCH NOTES ===")

        search_result = await client.call_tool(
            "search_notes",
            {
                "query": "What manages computer hardware and system resources?",
                "top_k": 3,
            },
        )

        print(search_result)

        print()

        print("=== LIST SOURCES ===")

        sources_result = await client.call_tool(
            "list_sources",
            {},
        )

        print(sources_result)

        print()

        print("=== GET DOCUMENT ===")

        document_result = await client.call_tool(
            "get_document",
            {
                "doc_id": "OS-1",
            },
        )

        print(document_result)


if __name__ == "__main__":
    asyncio.run(main())
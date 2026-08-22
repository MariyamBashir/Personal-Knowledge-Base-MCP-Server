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
                "user_id": "user_1",
                "top_k": 3,
            },
        )

        print(search_result)

        print()

        print("=== LIST SOURCES ===")

        sources_result = await client.call_tool(
            "list_sources",
            {
                "user_id": "user_1",
            },
        )

        print(sources_result)

        print()

        print("=== GET DOCUMENT ===")

        document_result = await client.call_tool(
            "get_document",
            {
                "doc_id": "OS-1",
                "user_id": "user_1",
            },
        )

        print(document_result)

        print()

        print("=== MULTI-USER ISOLATION ===")

        print("--- USER 1 SOURCES ---")

        user1_sources = await client.call_tool(
            "list_sources",
            {
                "user_id": "user_1",
            },
        )

        print(user1_sources)

        print()

        print("--- USER 2 SOURCES ---")

        user2_sources = await client.call_tool(
        "list_sources",
            {
                "user_id": "user_2",
            },
        )

        print(user2_sources)

        print()

        print("--- USER 1 SEARCHING FOR USER 2 CONTENT ---")

        user1_search = await client.call_tool(
        "search_notes",
            {   
                "query": "database indexing B-tree",
                "user_id": "user_1",
                "top_k": 5,
            },
        )

        print(user1_search)

        print()

        print("--- USER 2 SEARCHING FOR OWN CONTENT ---")

        user2_search = await client.call_tool(
        "search_notes",
            {
                "query": "database indexing B-tree",
                "user_id": "user_2",
                "top_k": 5,
            },
        )

        print(user2_search)


if __name__ == "__main__":
    asyncio.run(main())
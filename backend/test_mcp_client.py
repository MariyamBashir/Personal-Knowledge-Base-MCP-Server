import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "app.mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            print("\nConnected to MCP server!")

            tools = await session.list_tools()

            print("\nAvailable tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            print("\nCalling search_notes...\n")

            result = await session.call_tool(
                "search_notes",
                {
                    "query": "How do database indexes improve search performance?",
                    "top_k": 3,
                },
            )

            print("\nSearch Results:\n")

            if result.structuredContent:

                response = result.structuredContent

                if not response.get("results"):
                    print(response.get("message", "No results found."))
                    return

                for item in response["results"]:

                    print(f"Rank: {item['rank']}")
                    print(f"Score: {item['score']}")
                    print(f"Source: {item['source']}")
                    print(f"Subject: {item['subject']}")
                    print(f"Page: {item['page']}")
                    print(f"Text: {item['text'][:500]}...")
                    print("-" * 80)

            else:

                print("No structured content returned.")

                for item in result.content:
                    print(item)


if __name__ == "__main__":
    asyncio.run(main())
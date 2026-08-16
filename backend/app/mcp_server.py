import sys
import time

from fastmcp import FastMCP

from app.services.retrieval import search_documents


mcp = FastMCP("Personal Knowledge Base")


@mcp.tool()
def ping() -> str:
    """Simple connectivity test."""
    return "MCP server is working!"


@mcp.tool()
def search_notes(
    query: str,
    top_k: int = 5,
) -> dict:
    """
    Search the personal knowledge base using semantic search.

    Args:
        query: Natural-language question or search query.
        top_k: Maximum number of results to return.

    Returns:
        Ranked search results with source citations.
    """

    print(
        f"MCP: search_notes called with query: {query}",
        file=sys.stderr,
        flush=True,
    )

    start = time.time()

    results = search_documents(
        query=query,
        top_k=top_k,
    )

    elapsed = time.time() - start

    print(
        f"MCP: search completed in {elapsed:.2f}s",
        file=sys.stderr,
        flush=True,
    )

    if not results:
        return {
            "query": query,
            "results": [],
            "message": "No confident match found.",
        }

    formatted_results = []

    for rank, result in enumerate(results, start=1):
        formatted_results.append(
            {
                "rank": rank,
                "score": round(result["score"], 4),
                "source": result["filename"],
                "doc_id": result["doc_id"],
                "subject": result["subject"],
                "page": result["page_number"],
                "chunk": result["chunk_index"],
                "text": result["text"],
            }
        )

    return {
        "query": query,
        "results": formatted_results,
    }


if __name__ == "__main__":
    mcp.run()
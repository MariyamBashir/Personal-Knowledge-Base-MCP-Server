import sys
import time

from fastmcp import FastMCP

from app.services.retrieval import (
    search_documents,
    get_document as retrieve_document,
    list_sources as retrieve_sources,
)


mcp = FastMCP("Personal Knowledge Base")


@mcp.tool()
def ping() -> str:
    """Simple connectivity test."""
    return "MCP server is working!"


@mcp.tool()
def search_notes(
    query: str,
    user_id: str,
    top_k: int = 5,
) -> dict:
    """
    Search the personal knowledge base using semantic search.

    Args:
        query: Natural-language question or search query.
        user_id: Unique identifier of the user.
        top_k: Maximum number of results to return.

    Returns:
        Ranked search results with source citations.
    """

    print(
        f"MCP: search_notes called by user {user_id} "
        f"with query: {query}",
        file=sys.stderr,
        flush=True,
    )

    start = time.time()

    results = search_documents(
        query=query,
        top_k=top_k,
        user_id=user_id,
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
            "user_id": user_id,
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
        "user_id": user_id,
        "results": formatted_results,
    }


@mcp.tool()
def get_document(
    doc_id: str,
    user_id: str,
) -> dict:
    """
    Retrieve the complete content of a document from the knowledge base.

    Args:
        doc_id: Unique identifier of the document.
        user_id: Unique identifier of the user.

    Returns:
        Document metadata and reconstructed content.
    """

    print(
        f"MCP: get_document called by user {user_id} "
        f"with doc_id: {doc_id}",
        file=sys.stderr,
        flush=True,
    )

    start = time.time()

    document = retrieve_document(
        doc_id=doc_id,
        user_id=user_id,
    )

    elapsed = time.time() - start

    print(
        f"MCP: document retrieval completed in {elapsed:.2f}s",
        file=sys.stderr,
        flush=True,
    )

    if document is None:
        return {
            "doc_id": doc_id,
            "user_id": user_id,
            "found": False,
            "message": "Document not found.",
        }

    return {
        "found": True,
        "user_id": user_id,
        **document,
    }


@mcp.tool()
def list_sources(user_id: str) -> dict:
    """
    List all documents available to a specific user.

    Args:
        user_id: Unique identifier of the user.

    Returns:
        A list of unique documents with their IDs, filenames, and subjects.
    """

    print(
        f"MCP: list_sources called by user {user_id}",
        file=sys.stderr,
        flush=True,
    )

    start = time.time()

    sources = retrieve_sources(user_id=user_id)

    elapsed = time.time() - start

    print(
        f"MCP: source listing completed in {elapsed:.2f}s",
        file=sys.stderr,
        flush=True,
    )

    return {
        "user_id": user_id,
        "total_sources": len(sources),
        "sources": sources,
    }


if __name__ == "__main__":
    mcp.run()
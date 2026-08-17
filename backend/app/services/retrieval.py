from app.services.embeddings import generate_embedding
from app.services.qdrant_service import COLLECTION_NAME, get_client


SIMILARITY_THRESHOLD = 0.45


def search_documents(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Perform semantic search over the personal knowledge base.

    Results below the similarity threshold are discarded.
    """

    client = get_client()

    query_vector = generate_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    matches = []

    for result in results.points:

        if result.score < SIMILARITY_THRESHOLD:
            continue

        matches.append(
            {
                "score": result.score,
                "doc_id": result.payload.get("doc_id"),
                "filename": result.payload.get("filename"),
                "subject": result.payload.get("subject"),
                "page_number": result.payload.get("page_number"),
                "chunk_index": result.payload.get("chunk_index"),
                "text": result.payload.get("text"),
            }
        )

    return matches


def get_document(doc_id: str) -> dict | None:
    """
    Retrieve all chunks belonging to a document
    and reconstruct its content.
    """

    client = get_client()

    results, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter={
            "must": [
                {
                    "key": "doc_id",
                    "match": {
                        "value": doc_id,
                    },
                }
            ]
        },
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    if not results:
        return None

    chunks = []

    for result in results:
        payload = result.payload

        chunks.append(
            {
                "filename": payload.get("filename"),
                "subject": payload.get("subject"),
                "page_number": payload.get("page_number"),
                "chunk_index": payload.get("chunk_index"),
                "text": payload.get("text"),
            }
        )

    chunks.sort(
        key=lambda chunk: (
            chunk["page_number"] or 0,
            chunk["chunk_index"] or 0,
        )
    )

    document_text = "\n\n".join(
        chunk["text"]
        for chunk in chunks
        if chunk["text"]
    )

    return {
        "doc_id": doc_id,
        "filename": chunks[0]["filename"],
        "subject": chunks[0]["subject"],
        "total_chunks": len(chunks),
        "content": document_text,
        "chunks": chunks,
    }


def list_sources() -> list[dict]:
    """
    List all unique documents available
    in the personal knowledge base.
    """

    client = get_client()

    results, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    sources = {}

    for result in results:
        payload = result.payload

        doc_id = payload.get("doc_id")

        if not doc_id:
            continue

        if doc_id not in sources:
            sources[doc_id] = {
                "doc_id": doc_id,
                "filename": payload.get("filename"),
                "subject": payload.get("subject"),
            }

    return list(sources.values())
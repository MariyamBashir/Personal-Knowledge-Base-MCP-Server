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
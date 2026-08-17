from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.retrieval import (
    search_documents,
    get_document,
    list_sources,
)


class Source(BaseModel):
    doc_id: str
    filename: str
    subject: str


class SourcesResponse(BaseModel):
    total_sources: int
    sources: list[Source]


app = FastAPI(
    title="Personal Knowledge Base API",
    description="HTTP API for the Personal Knowledge MCP Server",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Personal Knowledge Base API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/search")
def search(
    query: str = Query(
        ...,
        min_length=1,
        description="Natural-language search query",
    ),
    top_k: int = Query(
        5,
        ge=1,
        le=20,
        description="Maximum number of results",
    ),
):
    results = search_documents(
        query=query,
        top_k=top_k,
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

@app.get("/sources", response_model=SourcesResponse)
def sources():
    """Return all documents available in the knowledge base."""

    documents = list_sources()

    return {
        "total_sources": len(documents),
        "sources": documents,
    }


@app.get("/documents/{doc_id}")
def document(doc_id: str):
    """Return the complete content of a document."""

    result = get_document(doc_id)

    if result is None:
        return {
            "found": False,
            "doc_id": doc_id,
            "message": "Document not found.",
        }

    return {
        "found": True,
        **result,
    }
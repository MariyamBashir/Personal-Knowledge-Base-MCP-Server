from pathlib import Path

from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services.ingestion import ingest_pdf
from app.services.retrieval import (
    search_documents,
    get_document,
    list_sources,
)

UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

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

@app.post("/upload")
async def upload_document(
    user_id: str = Query(
        ...,
        min_length=1,
        description="Unique identifier of the user",
    ),
    subject: str = Query(
        ...,
        min_length=1,
        description="Subject/category of the document",
    ),
    file: UploadFile = File(...),
):
    """Upload and ingest a PDF for a specific user."""

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    subject_dir = UPLOADS_DIR / subject
    subject_dir.mkdir(parents=True, exist_ok=True)

    file_path = subject_dir / file.filename

    contents = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    chunks_stored = ingest_pdf(
        file_path=file_path,
        user_id=user_id,
    )

    if chunks_stored == 0:
        return {
            "success": False,
            "user_id": user_id,
            "filename": file.filename,
            "message": "No text found in the PDF.",
        }

    return {
        "success": True,
        "user_id": user_id,
        "filename": file.filename,
        "subject": subject,
        "chunks_stored": chunks_stored,
        "message": "Document uploaded and ingested successfully.",
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
    user_id: str = Query(
        ...,
        min_length=1,
        description="Unique identifier of the user",
    ),
):
    results = search_documents(
        query=query,
        top_k=top_k,
        user_id=user_id,
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


@app.get("/sources", response_model=SourcesResponse)
def sources(
    user_id: str = Query(
        ...,
        min_length=1,
        description="Unique identifier of the user",
    ),
):
    """Return all documents available to the specified user."""

    documents = list_sources(user_id=user_id)

    return {
        "total_sources": len(documents),
        "sources": documents,
    }


@app.get("/documents/{doc_id}")
def document(
    doc_id: str,
    user_id: str = Query(
        ...,
        min_length=1,
        description="Unique identifier of the user",
    ),
):
    """Return the complete content of a document for the specified user."""

    result = get_document(
        doc_id=doc_id,
        user_id=user_id,
    )

    if result is None:
        return {
            "found": False,
            "doc_id": doc_id,
            "user_id": user_id,
            "message": "Document not found.",
        }

    return {
        "found": True,
        "user_id": user_id,
        **result,
    }
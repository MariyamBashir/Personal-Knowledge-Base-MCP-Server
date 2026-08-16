from pathlib import Path
from uuid import uuid4

from qdrant_client.models import PointStruct

from app.services.chunker import split_text_into_chunks
from app.services.embeddings import generate_embeddings
from app.services.qdrant_service import COLLECTION_NAME, get_client
from app.utils.document_reader import read_pdf_pages


UPLOADS_DIR = Path("uploads")


def ingest_pdf(file_path: Path) -> int:
    """
    Read a PDF, create chunks, generate embeddings,
    and store the chunks in Qdrant.

    Returns:
        Number of chunks stored.
    """

    client = get_client()

    pages = read_pdf_pages(file_path)

    all_chunks = []

    for page in pages:
        page_number = page["page_number"]
        page_text = page["text"]

        chunks = split_text_into_chunks(page_text)

        for chunk_index, chunk_text in enumerate(chunks):

            all_chunks.append(
                {
                    "doc_id": file_path.stem,
                    "filename": file_path.name,
                    "subject": file_path.parent.name,
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "text": chunk_text,
                }
            )

    if not all_chunks:
        print(f"No text found in {file_path.name}")
        return 0

    texts = [chunk["text"] for chunk in all_chunks]

    embeddings = generate_embeddings(texts)

    points = []

    for chunk, embedding in zip(all_chunks, embeddings):

        point = PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload=chunk,
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(
        f"Ingested {file_path.name}: "
        f"{len(points)} chunks"
    )

    return len(points)


def ingest_all_documents() -> int:
    """Ingest every PDF inside the uploads directory."""

    pdf_files = sorted(UPLOADS_DIR.rglob("*.pdf"))

    total_chunks = 0

    print(f"Found {len(pdf_files)} PDF files.")
    print()

    for file_path in pdf_files:
        total_chunks += ingest_pdf(file_path)

    print()
    print(f"Total chunks stored: {total_chunks}")

    return total_chunks
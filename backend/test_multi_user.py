from pathlib import Path

from app.services.ingestion import ingest_all_documents
from app.services.retrieval import (
    search_documents,
    get_document,
    list_sources,
)


TEST_USER = "user_1"


print("=" * 50)
print("MULTI-USER TEST")
print("=" * 50)

print("\n=== INGESTING DOCUMENTS ===")

total_chunks = ingest_all_documents(TEST_USER)

print(f"\nTotal chunks ingested: {total_chunks}")


print("\n=== LIST SOURCES ===")

sources = list_sources(TEST_USER)

print(f"Sources found: {len(sources)}")

for source in sources:
    print(
        f"- {source['doc_id']} | "
        f"{source['filename']} | "
        f"{source['subject']}"
    )


print("\n=== SEARCH ===")

results = search_documents(
    query="What manages computer hardware and system resources?",
    user_id=TEST_USER,
    top_k=5,
)

for rank, result in enumerate(results, start=1):
    print(
        f"#{rank} "
        f"{result['filename']} "
        f"score={result['score']:.4f}"
    )


print("\n=== GET DOCUMENT ===")

document = get_document(
    doc_id="OS-1",
    user_id=TEST_USER,
)

if document:
    print(
        f"Found: {document['filename']} | "
        f"chunks={document['total_chunks']}"
    )
else:
    print("Document not found.")


print("\n=== ISOLATION TEST ===")

fake_user_results = search_documents(
    query="What manages computer hardware and system resources?",
    user_id="user_2",
    top_k=5,
)

print(
    f"user_2 search results: "
    f"{len(fake_user_results)}"
)

fake_document = get_document(
    doc_id="OS-1",
    user_id="user_2",
)

print(
    "user_2 OS-1 access:",
    "ALLOWED" if fake_document else "BLOCKED",
)

fake_sources = list_sources("user_2")

print(
    f"user_2 sources: {len(fake_sources)}"
)
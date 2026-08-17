from app.services.retrieval import get_document, list_sources


print("=== LIST SOURCES ===")

sources = list_sources()

print(f"Total sources: {len(sources)}")

for source in sources:
    print(source)


print()
print("=== GET DOCUMENT ===")

document = get_document("ADS-2")

if document is None:
    print("Document not found.")
else:
    print(f"Document ID: {document['doc_id']}")
    print(f"Filename: {document['filename']}")
    print(f"Subject: {document['subject']}")
    print(f"Total chunks: {document['total_chunks']}")
    print()
    print(document["content"][:1000])
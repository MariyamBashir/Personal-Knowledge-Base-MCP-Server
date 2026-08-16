from pathlib import Path

from app.utils.document_reader import read_pdf_pages
from app.services.chunker import split_text_into_chunks


file_path = Path("uploads/ADS/ADS-2.pdf")

pages = read_pdf_pages(file_path)

print(f"Document: {file_path.name}")
print(f"Pages: {len(pages)}")
print("=" * 60)

total_chunks = 0

for page in pages:
    chunks = split_text_into_chunks(page["text"])

    print(f"\nPage {page['page_number']}")
    print(f"Words: {len(page['text'].split())}")
    print(f"Chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks):
        print(f"\nChunk {index}")
        print(f"Words: {len(chunk.split())}")
        print(chunk[:300])

    total_chunks += len(chunks)

print("\n" + "=" * 60)
print(f"TOTAL CHUNKS: {total_chunks}")
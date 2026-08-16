from pathlib import Path

from app.utils.document_reader import get_document_info


uploads_dir = Path("uploads")

pdf_files = sorted(uploads_dir.rglob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files")
print("=" * 60)

total_words = 0

for file_path in pdf_files:
    document = get_document_info(file_path)

    print(f"Subject: {document['subject']}")
    print(f"File: {document['filename']}")
    print(f"Characters: {document['character_count']}")
    print(f"Words: {document['word_count']}")
    print("-" * 60)

    total_words += document["word_count"]

print()
print("=" * 60)
print(f"TOTAL WORDS: {total_words}")
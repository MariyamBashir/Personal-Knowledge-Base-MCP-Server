from pathlib import Path

from pypdf import PdfReader


SUPPORTED_EXTENSIONS = {".pdf", ".md", ".txt"}


def read_pdf_pages(file_path: Path) -> list[dict]:
    """Extract text from a PDF while preserving page information."""

    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        text = text.strip()

        if text:
            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

    return pages


def read_pdf(file_path: Path) -> str:
    """Extract all text from a PDF."""

    pages = read_pdf_pages(file_path)

    return "\n\n".join(page["text"] for page in pages)


def read_text_file(file_path: Path) -> str:
    """Read text from a Markdown or TXT file."""

    return file_path.read_text(encoding="utf-8").strip()


def read_document(file_path: Path) -> str:
    """Read a supported document and return its text."""

    extension = file_path.suffix.lower()

    if extension == ".pdf":
        return read_pdf(file_path)

    if extension in {".md", ".txt"}:
        return read_text_file(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        f"Supported types: {SUPPORTED_EXTENSIONS}"
    )


def get_document_info(file_path: Path) -> dict:
    """Return basic metadata about a document."""

    text = read_document(file_path)

    return {
        "doc_id": file_path.stem,
        "filename": file_path.name,
        "subject": file_path.parent.name,
        "file_type": file_path.suffix.lower(),
        "text": text,
        "character_count": len(text),
        "word_count": len(text.split()),
    }
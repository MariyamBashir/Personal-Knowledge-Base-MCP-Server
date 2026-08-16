import re


def clean_text(text: str) -> str:
    """Clean extracted PDF text while preserving paragraph structure."""

    # Normalize whitespace within lines
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_into_paragraphs(text: str) -> list[str]:
    """Split text into meaningful paragraphs/sections."""

    text = clean_text(text)

    paragraphs = re.split(r"\n\s*\n", text)

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


def split_text_into_chunks(
    text: str,
    chunk_size: int = 160,
    overlap: int = 30,
) -> list[str]:
    """
    Split text into chunks while trying to preserve paragraph boundaries.

    Small documents remain as a single chunk.
    Larger documents are combined into chunks close to the target size.
    """

    paragraphs = split_into_paragraphs(text)

    if not paragraphs:
        return []

    chunks = []
    current_words = []

    for paragraph in paragraphs:
        paragraph_words = paragraph.split()

        # If adding this paragraph keeps us within the target size,
        # keep it together.
        if (
            current_words
            and len(current_words) + len(paragraph_words) <= chunk_size
        ):
            current_words.extend(paragraph_words)
            continue

        # Save the current chunk before starting a new one.
        if current_words:
            chunks.append(" ".join(current_words))

            # Keep some words from the previous chunk as overlap.
            overlap_words = current_words[-overlap:]
            current_words = overlap_words.copy()

        # If a single paragraph is larger than the target,
        # split that paragraph into smaller pieces.
        if len(paragraph_words) > chunk_size:
            start = 0

            while start < len(paragraph_words):
                end = start + chunk_size
                piece = paragraph_words[start:end]

                if piece:
                    chunks.append(" ".join(piece))

                if end >= len(paragraph_words):
                    break

                start = end - overlap

            current_words = []
        else:
            current_words.extend(paragraph_words)

    # Add remaining words.
    if current_words:
        chunks.append(" ".join(current_words))

    return chunks
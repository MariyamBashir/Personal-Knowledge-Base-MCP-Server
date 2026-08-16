import os

# Silence Hugging Face / Transformers messages
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

# Model is NOT loaded when this module is imported.
model = None


def get_model() -> SentenceTransformer:
    """Load the embedding model only when it is first needed."""

    global model

    if model is None:
        print("Loading embedding model...", flush=True)

        model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded!", flush=True)

    return model


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding vector for a single text."""

    embedding_model = get_model()

    embedding = embedding_model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embedding vectors for multiple texts."""

    embedding_model = get_model()

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True,
    )

    return embeddings.tolist()
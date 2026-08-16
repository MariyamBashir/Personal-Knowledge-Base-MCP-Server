from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import QDRANT_URL, QDRANT_API_KEY


COLLECTION_NAME = "personal_knowledge"
VECTOR_SIZE = 384


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)


def create_collection() -> None:
    """Create the personal knowledge collection if it does not exist."""

    existing_collections = client.get_collections()

    collection_names = {
        collection.name
        for collection in existing_collections.collections
    }

    if COLLECTION_NAME in collection_names:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )

    print(f"Collection '{COLLECTION_NAME}' created successfully!")


def get_client() -> QdrantClient:
    """Return the Qdrant client."""

    return client
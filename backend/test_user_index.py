from app.services.qdrant_service import get_client, COLLECTION_NAME
from qdrant_client.models import PayloadSchemaType


client = get_client()

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="user_id",
    field_schema=PayloadSchemaType.KEYWORD,
)

print("user_id index created successfully!")
from qdrant_client.models import PayloadSchemaType

from app.services.qdrant_service import COLLECTION_NAME, get_client


client = get_client()

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="doc_id",
    field_schema=PayloadSchemaType.KEYWORD,
)

print("Payload index created successfully for 'doc_id'.")
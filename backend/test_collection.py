from app.services.qdrant_service import (
    COLLECTION_NAME,
    create_collection,
    get_client,
)


create_collection()

client = get_client()

collections = client.get_collections()

print()
print("Available collections:")

for collection in collections.collections:
    print(f"- {collection.name}")

print()
print(f"Project 3 collection: {COLLECTION_NAME}")
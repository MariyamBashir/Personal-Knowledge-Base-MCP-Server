from app.services.qdrant_service import COLLECTION_NAME, get_client


client = get_client()

collection_info = client.get_collection(COLLECTION_NAME)

print("Collection:", COLLECTION_NAME)
print("Points:", collection_info.points_count)
print("Vector size:", collection_info.config.params.vectors.size)
print()

print("Sample stored points:")
print("=" * 60)

results = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=5,
    with_payload=True,
    with_vectors=True,
)

points, _ = results

for index, point in enumerate(points, start=1):
    print(f"\nPoint {index}")
    print("ID:", point.id)

    print("Payload:")
    for key, value in point.payload.items():
        if key == "text":
            print(f"  {key}: {value[:200]}...")
        else:
            print(f"  {key}: {value}")

    if point.vector is not None:
        print("Vector dimensions:", len(point.vector))

print()
print("=" * 60)
print("Qdrant verification complete!")
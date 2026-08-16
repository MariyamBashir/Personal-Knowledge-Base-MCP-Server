from app.services.embeddings import generate_embedding


text = """
An operating system manages computer hardware and system resources.
It handles processes, memory, files, and communication between
applications and hardware.
"""


embedding = generate_embedding(text)

print("Embedding generated successfully!")
print(f"Vector dimensions: {len(embedding)}")
print(f"First 10 values: {embedding[:10]}")
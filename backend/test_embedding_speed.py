import time

from app.services.embeddings import get_model, generate_embedding


print("Loading model...")

start = time.perf_counter()

model = get_model()

load_time = time.perf_counter() - start

print(f"Model load time: {load_time:.2f} seconds")

print()
print("Generating embedding...")

start = time.perf_counter()

vector = generate_embedding(
    "What is the role of the kernel in an operating system?"
)

embedding_time = time.perf_counter() - start

print(f"Embedding generation time: {embedding_time:.4f} seconds")
print(f"Vector dimensions: {len(vector)}")
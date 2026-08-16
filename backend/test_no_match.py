from app.services.retrieval import search_documents


query = "What are the causes of climate change?"

results = search_documents(query, top_k=5)

print(f"Query: {query}")
print("=" * 70)

if not results:
    print("No confident match found.")
else:
    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(f"Score: {result['score']:.4f}")
        print(f"Source: {result['filename']}")
        print(f"Subject: {result['subject']}")
        print(f"Page: {result['page_number']}")
        print(f"Text: {result['text'][:300]}")
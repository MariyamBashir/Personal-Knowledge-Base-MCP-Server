from app.services.retrieval import search_documents


queries = [
    "What are the causes of climate change?",
    "How does photosynthesis work in plants?",
    "What are the health benefits of regular exercise?",
    "Explain the history of the Roman Empire.",
    "How do earthquakes occur?",
]


for query in queries:
    results = search_documents(query, top_k=3)

    print("\n" + "=" * 80)
    print(f"Query: {query}")
    print("-" * 80)

    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. "
            f"{result['filename']} | "
            f"Subject: {result['subject']} | "
            f"Score: {result['score']:.4f}"
        )
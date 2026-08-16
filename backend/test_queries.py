from app.services.retrieval import search_documents


queries = [
    {
        "query": "What are the main responsibilities of an operating system?",
        "expected_subject": "OS",
    },
    {
        "query": "How does an operating system manage CPU and memory?",
        "expected_subject": "OS",
    },
    {
        "query": "What is the role of the kernel in an operating system?",
        "expected_subject": "OS",
    },
    {
        "query": "How do computers communicate and exchange information?",
        "expected_subject": "CCN",
    },
    {
        "query": "What is a VPN and how does it provide secure communication?",
        "expected_subject": "CCN",
    },
    {
        "query": "What are common networking protocols and devices?",
        "expected_subject": "CCN",
    },
    {
        "query": "How does database normalization reduce redundant data?",
        "expected_subject": "ADS",
    },
    {
        "query": "How do database indexes improve search performance?",
        "expected_subject": "ADS",
    },
    {
        "query": "What are primary keys and foreign keys used for?",
        "expected_subject": "ADS",
    },
]


for item in queries:
    query = item["query"]
    expected = item["expected_subject"]

    results = search_documents(query, top_k=3)

    print("\n" + "=" * 80)
    print(f"Query: {query}")
    print(f"Expected subject: {expected}")
    print("-" * 80)

    for rank, result in enumerate(results, start=1):
        print(
            f"{rank}. "
            f"{result['filename']} | "
            f"Subject: {result['subject']} | "
            f"Score: {result['score']:.4f}"
        )
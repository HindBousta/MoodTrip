from src.retrieval.retrieve import retrieve_places

query = "outdoor adventure hiking"
print(f"Retrieving places for query: '{query}'")
results = retrieve_places(query, top_k=3)
print(results)

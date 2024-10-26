import chromadb

# Create a persistent client
persistent_client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection
collection = persistent_client.create_collection("qa_collection")

# Add some question-answer pairs
collection.add(
    documents=[
        "The capital of France is Paris.",
        "The largest planet in our solar system is Jupiter.",
        "The chemical symbol for gold is Au.",
    ],
    metadatas=[
        {"type": "geography"},
        {"type": "astronomy"},
        {"type": "chemistry"},
    ],
    ids=["1", "2", "3"]
)

# Query the collection with a similar question
query = "What's the biggest planet?"
results = collection.query(
    query_texts=[query],
    n_results=1
)

# Print the results
print(f"Query: {query}")
print(f"Most similar document: {results['documents'][0][0]}")
print(f"Distance: {results['distances'][0][0]}")

# Clean up (optional)
persistent_client.delete_collection("qa_collection")

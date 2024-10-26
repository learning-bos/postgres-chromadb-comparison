import chromadb
import time

# Create a persistent client
persistent_client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection
collection = persistent_client.create_collection("qa_collection")

# Add some question-answer pairs
collection.add(
    documents=[
        "A group of vibrant parrots chatter loudly, sharing stories of their tropical adventures.",
        "The mathematician found solace in numbers, deciphering the hidden patterns of the universe.",
        "The robot, with its intricate circuitry and precise movements, assembles the devices swiftly.",
        "The chef, with a sprinkle of spices and a dash of love, creates culinary masterpieces.",
        "The ancient tree, with its gnarled branches and deep roots, whispers secrets of the past.",
        "The detective, with keen observation and logical reasoning, unravels the intricate web of clues.",
        "The sunset paints the sky with shades of orange, pink, and purple, reflecting on the calm sea.",
        "In the dense forest, the howl of a lone wolf echoes, blending with the symphony of the night.",
        "The dancer, with graceful moves and expressive gestures, tells a story without uttering a word.",
        "In the quantum realm, particles flicker in and out of existence, dancing to the tunes of probability.",
    ],
    ids=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
)

# Query the collection with a similar question
query = "Give me some content about the ocean"
time_start = time.time()
results = collection.query(
    query_texts=[query],
    n_results=3
)
time_end = time.time()

print(f"Time taken: {time_end - time_start} seconds\n")

# Print the results
print(f"Query: {query}")

for index, x in enumerate(results['documents'][0]):
    print(f"Most similar document: {x}\n")
    print(f"Distance: {results['distances'][0][index]}\n")
    print("==============================================\n")


# Clean up (optional)
persistent_client.delete_collection("qa_collection")

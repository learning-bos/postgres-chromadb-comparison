import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')
'''

# Connect to your PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="vector_db",
    user="postgres",
    password="postgres"
)
# Create a cursor
cur = conn.cursor()
# Enable pgvector extension if not already enabled
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
# Create the table with a vector column (if it doesn't exist)
cur.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id SERIAL PRIMARY KEY,
        text TEXT,
        embedding vector(384)
    )
""")

# Sample texts to embed
texts = [
    "The capital of France is Paris.",
    "The largest planet in our solar system is Jupiter.",
    "The chemical symbol for gold is Au.",
]

# Create embeddings
embeddings = model.encode(texts)

# Prepare data for insertion
data = [(text, embedding.tolist()) for text, embedding in zip(texts, embeddings)]

# Insert data into the table
execute_values(cur, """
    INSERT INTO embeddings (text, embedding)
    VALUES %s
""", data, template="(%s, %s::vector)")

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
'''
print("Embeddings stored successfully!")

# Query the collection with a similar question
query = "What's the biggest planet?"
# Create a new connection and cursor for querying
conn = psycopg2.connect(
    host="localhost",
    database="vector_db",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# Encode the query
query_embedding = model.encode([query])[0]
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
# Perform the similarity search
cur.execute("""
    SELECT text, 1 - (embedding <=> %s) AS cosine_similarity
    FROM embeddings
    ORDER BY embedding <=> %s
    LIMIT 1
""", (query_embedding.tolist(), query_embedding.tolist()))

# Fetch the result
result = cur.fetchone()

if result:
    most_similar_text, similarity = result
    print(f"Query: {query}")
    print(f"Most similar document: {most_similar_text}")
    print(f"Cosine similarity: {similarity}")
else:
    print("No results found.")

# Close the cursor and connection
cur.close()
conn.close()

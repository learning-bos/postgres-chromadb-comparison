import psycopg2
from psycopg2.extras import execute_values
import numpy as np
from sentence_transformers import SentenceTransformer

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="vector_db",
    user="postgres",
    password="postgres"
)
cur = conn.cursor()

# Enable pgvector extension if not already enabled
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

# Create a table for our vector store
cur.execute("""
    CREATE TABLE IF NOT EXISTS qa_collection (
        id SERIAL PRIMARY KEY,
        document TEXT,
        embedding VECTOR(384),
        metadata JSONB
    )
""")

# Create an index for faster similarity search
cur.execute("CREATE INDEX IF NOT EXISTS qa_collection_embedding_idx ON qa_collection USING ivfflat (embedding vector_cosine_ops)")

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Add some question-answer pairs
documents = [
    "The capital of France is Paris.",
    "The largest planet in our solar system is Jupiter.",
    "The chemical symbol for gold is Au.",
]
metadatas = [
    {"type": "geography"},
    {"type": "astronomy"},
    {"type": "chemistry"},
]

# Generate embeddings
embeddings = model.encode(documents)

# Insert data into the table
insert_query = """
    INSERT INTO qa_collection (document, embedding, metadata)
    VALUES %s
"""
insert_data = [
    (doc, embedding.tolist(), metadata)
    for doc, embedding, metadata in zip(documents, embeddings, metadatas)
]
print(type(insert_data))
execute_values(cur, insert_query, insert_data)

# Commit the changes
conn.commit()

# Query the collection with a similar question
query = "What's the biggest planet?"
query_embedding = model.encode([query])[0]

# Perform similarity search
cur.execute("""
    SELECT document, 1 - (embedding <=> %s) AS similarity
    FROM qa_collection
    ORDER BY similarity DESC
    LIMIT 1
""", (query_embedding.tolist(),))

result = cur.fetchone()

# Print the results
print(f"Query: {query}")
print(f"Most similar document: {result[0]}")
print(f"Similarity: {result[1]}")

# Clean up (optional)
cur.execute("DROP TABLE IF EXISTS qa_collection")
conn.commit()

# Close the database connection
cur.close()
conn.close()

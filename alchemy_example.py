import time
from sqlalchemy import DateTime, create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from embedding_util import generate_embeddings
from sqlalchemy.sql import func

Base = declarative_base()
N_DIM = 384

class TextEmbedding(Base):
    __tablename__ = 'text_embeddings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    additional_metadata = Column(JSONB)
    context = Column(Text)
    created_at = Column(DateTime, server_default = func.now())
    embedding = Column(Vector(N_DIM))

# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:postgres@localhost:5432/vector_db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def insert_embeddings(content, additional_metadata, context):
    embedding = generate_embeddings(content)
    
    new_embedding = TextEmbedding(
        content=content, 
        additional_metadata=additional_metadata, 
        context=context, 
        embedding=embedding
    )
    session.add(new_embedding)
    session.commit()

def insert_all_embeddings():
    sentences = [
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
    ]
    for sentence in sentences:
        insert_embeddings(sentence, {}, "context1")

def find_similar_embeddings(query, limit=1):
    query_embedding = generate_embeddings(query)
    # a similarity threshold can be setted
    # similarity_threshold = 0.7
    result = session.query(TextEmbedding, 
                           TextEmbedding.
                           embedding.
                           cosine_distance(query_embedding).
                           label("distance")).order_by("distance").limit(limit).all()
    
    '''insert the following after "label("distance"))".filter(TextEmbedding.embedding.cosine_distance(query_embedding) < similarity_threshold)'''
    if len(result) == 0:
        return None
    else:
        return result[0][0]

# insert_all_embeddings()

time_start = time.time()
result = find_similar_embeddings("Give me some content about the ocean")
time_end = time.time()
print(f"Time taken: {time_end - time_start} seconds")

# the test show that the time is the same as using the plain test_postgres.py

if result is not None:
    print(result.content)
else:
    print("No similar embeddings found")



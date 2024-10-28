from sqlalchemy import DateTime, create_engine, Column, Integer, JSON, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from embedding_util import generate_embeddings
from sqlalchemy.sql import func

Base = declarative_base()
N_DIM = 384

class TextEmbedding(Base):
    __tablename__ = 'text_embeddings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    additional_metadata = Column(JSON)
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

#insert_embeddings("Hello, 'ciao' \"ciao\"world!", {"source": "test"}, "This is a test")
def find_similar_embeddings(query, limit=1):
    query_embedding = generate_embeddings(query)
    result = session.query(TextEmbedding, TextEmbedding.embedding.cosine_distance(query_embedding).label("distance")).order_by("distance").limit(limit).all()
    return result

print(find_similar_embeddings("world")[0][0].content)

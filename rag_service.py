from models import DocumentChunk
from embeddings import get_embeddings
from chunking import chunk_text
from sqlalchemy.orm import Session
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("groq_api_key")
if not api_key:
    raise RuntimeError("groq api key not found please check your .env file!")
client = Groq(api_key=api_key)


SYSTEM_PROMPT = """You are a helpful assistant that answers questions based strictly on the provided context.

Rules:
- Only use information from the context to answer
- If the answer is not in the context, say "I don't have enough information to answer this"
- Be concise and accurate
- Never make up or invent information not present in the context"""



def store_documents(text : str,db : Session,source : str = None):
    chunks = chunk_text(text)
    for chunk in chunks:
        embeddings = get_embeddings(chunk)
        doc_chunk = DocumentChunk(content = chunk,embedding = embeddings,source = source)
        db.add(doc_chunk)
    db.commit()

def retrieve_chunks(query : str, db : Session,top_k : int = 3,source : str = None):
    query_embeddings = get_embeddings(query)
    db_query = db.query(DocumentChunk)
    if source:
        db_query = db_query.filter(DocumentChunk.source == source)

    results = db_query.order_by(DocumentChunk.embedding.l2_distance(query_embeddings)).limit(top_k).all()
    return [r.content for r in results]


def generate_answer(query : str, db : Session,source : str = None):
    chunking = retrieve_chunks(query,db)
    context  = "\n\n".join(chunking)
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages= [{"role" : "system" , "content" : SYSTEM_PROMPT},
                   {"role" : "user", "content" : f"Context:\n{context}\n\nQuestion: {query}"}
                   ],
        reasoning_effort = "low"
        
    )
    return response.choices[0].message.content
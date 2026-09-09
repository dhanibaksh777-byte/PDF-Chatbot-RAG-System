from pgvector.sqlalchemy import Vector
from sqlalchemy import Column,BigInteger,Text,String
from database import base


class DocumentChunk(base):
    __tablename__ = "document_chunks"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    content = Column(Text)
    embedding = Column(Vector(768))
    source  = Column(Text,nullable=True)


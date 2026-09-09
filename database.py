from  sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

database_url = os.getenv("database_url")
engine = create_engine(database_url,pool_pre_ping=True)
SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind=engine)
base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

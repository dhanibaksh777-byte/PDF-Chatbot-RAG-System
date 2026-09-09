from fastapi import FastAPI,Depends
from rag_service import store_documents,generate_answer
from sqlalchemy.orm import Session
from database import get_db
from pydantic import BaseModel
from fastapi import UploadFile,File
from pdf_extractor import extract_text_from_pdf
import shutil
from fastapi.middleware.cors import CORSMiddleware 
from database import engine,base
import os
import models


base.metadata.create_all(bind=engine)

class AskQuery(BaseModel):
    query : str
    source : str = None


class DocumentInput(BaseModel):
    source : str = None


app = FastAPI(title="RAG SERVICE")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/store-pdf")
def store_docs(file : UploadFile = File(...),source : str = None,db : Session = Depends(get_db)):
    with open("temp.pdf","wb") as f:
        shutil.copyfileobj(file.file,f)
    text = extract_text_from_pdf("temp.pdf")
    os.remove("temp.pdf")
    store_documents(text,db,source)
    return {"message" : "document stored successfully!"}


@app.post("/ask")
def ask(input : AskQuery, db : Session = Depends(get_db)):
    final_answer = generate_answer(input.query,db,input.source)
    return {"Answer" : final_answer}
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from . import models, schemas
from .database import engine, get_db

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doc Finder API",
    description="Backend API for Doc Finder Mobile App",
    version=os.getenv("API_VERSION", "v1")
)

@app.get("/documents/", response_model=List[schemas.Document])
def get_documents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of documents with pagination support.
    """
    documents = db.query(models.Document).offset(skip).limit(limit).all()
    return documents

@app.post("/documents/", response_model=schemas.Document, status_code=201)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    """
    Create a new document.
    """
    db_document = models.Document(**document.dict())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"} 
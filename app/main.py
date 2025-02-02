from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv
import uvicorn

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

@app.get("/doctors/", response_model=List[schemas.Doctor])
def get_doctors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of doctors with pagination support.
    """
    doctors = db.query(models.Doctor).offset(skip).limit(limit).all()
    return doctors

@app.post("/doctors/", response_model=schemas.Doctor, status_code=201) 
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """
    Create a new doctor.
    """
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

@app.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 

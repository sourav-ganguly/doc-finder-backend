from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv
import uvicorn
import json
from datetime import datetime

from . import models, schemas
from .database import engine, get_db

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Doc Finder API",
    description="Backend API for Doc Finder Mobile App",
    version=os.getenv("API_VERSION", "v1")
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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
def get_doctors(
    skip: int = 0, 
    limit: int = 10, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of doctors with pagination support.
    Optional search parameter to filter doctors by name, specialty, location, or educational degree.
    """
    query = db.query(models.Doctor)
    
    if search:
        # Convert search term to lowercase for case-insensitive search
        search = f"%{search.lower()}%"
        query = query.filter(
            # Using or_ to match any of the conditions
            models.Doctor.name.ilike(search) |
            models.Doctor.speciality.ilike(search) |
            models.Doctor.location.ilike(search) |
            models.Doctor.educational_degree.ilike(search)
        )
    
    doctors = query.offset(skip).limit(limit).all()
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

@app.post("/admin/import-doctors")
def import_doctors(db: Session = Depends(get_db)):
    """
    Import doctors from the JSON file if they don't already exist in the database.
    """
    try:
        # Read the JSON file
        with open("doctor_data/doctor-list-square-v2.json", "r") as f:
            doctors_data = json.load(f)

        imported_count = 0
        skipped_count = 0

        for doctor in doctors_data:
            # Check if doctor already exists by name and speciality
            existing_doctor = db.query(models.Doctor).filter(
                models.Doctor.name == doctor["name"],
                models.Doctor.speciality == doctor["specialty"]
            ).first()

            if existing_doctor:
                skipped_count += 1
                continue

            # Create new doctor object
            new_doctor = models.Doctor(
                name=doctor["name"],
                speciality=doctor["specialty"],
                educational_degree=doctor.get("educationalDegree"),
                description=doctor.get("description"),
                location=doctor.get("location"),
                data_source=doctor.get("dataSource"),
                data_scrapped_at=datetime.strptime(doctor["dataScrappedAt"], "%Y-%m-%d") if doctor.get("dataScrappedAt") else None
            )

            db.add(new_doctor)
            imported_count += 1

        db.commit()

        return {
            "message": "Import completed successfully",
            "imported": imported_count,
            "skipped": skipped_count
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv
import uvicorn
import json
from datetime import datetime
from sqlalchemy import or_

from . import models, schemas
from .database import engine, get_db
from .symptoms_matcher import match_specialization

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

@app.get("/get-speciality")
def get_speciality(symptoms: str):
    """
    Get medical specializations based on symptoms
    """
    try:
        specializations = match_specialization(symptoms)
        return {"specializations": specializations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctors/", response_model=List[schemas.Doctor])
def get_doctors(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of doctors with pagination support.
    Optional search parameter to filter doctors by name, specialty, location, or educational degree.
    Optional symptoms parameter to filter doctors by matching specializations.
    """
    query = db.query(models.Doctor)
    
    if search:
        # Get specializations from symptoms
        specializations = match_specialization(search).split(';')
        # Clean up any whitespace
        specializations = [spec.strip() for spec in specializations]
        
        # Create a filter for each specialization
        specialty_filters = [models.Doctor.speciality.ilike(f"%{spec}%") for spec in specializations]
        query = query.filter(or_(*specialty_filters))
    
    
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
    Import doctors from the JSON file. If a doctor already exists, replace with new data.
    """
    try:
        # Read the JSON file
        with open("doctor_data/doctor-list-square-v2.json", "r") as f:
            doctors_data = json.load(f)

        imported_count = 0
        updated_count = 0

        for doctor in doctors_data:
            # Check if doctor already exists by name and speciality
            existing_doctor = db.query(models.Doctor).filter(
                models.Doctor.name == doctor["name"],
                models.Doctor.speciality == doctor["specialty"]
            ).first()

            if existing_doctor:
                # Update existing doctor with new data
                existing_doctor.educational_degree = doctor.get("educationalDegree")
                existing_doctor.description = doctor.get("description")
                existing_doctor.location = doctor.get("location")
                existing_doctor.data_source = doctor.get("dataSource")
                existing_doctor.data_scrapped_at = datetime.strptime(doctor["dataScrappedAt"], "%Y-%m-%d") if doctor.get("dataScrappedAt") else None
                existing_doctor.clinics = doctor.get("clinics", [])
                existing_doctor.chambers = doctor.get("chambers", [])
                updated_count += 1
            else:
                # Create new doctor object
                new_doctor = models.Doctor(
                    name=doctor["name"],
                    speciality=doctor["specialty"],
                    educational_degree=doctor.get("educationalDegree"),
                    description=doctor.get("description"),
                    location=doctor.get("location"),
                    data_source=doctor.get("dataSource"),
                    data_scrapped_at=datetime.strptime(doctor["dataScrappedAt"], "%Y-%m-%d") if doctor.get("dataScrappedAt") else None,
                    clinics=doctor.get("clinics", []),
                    chambers=doctor.get("chambers", [])
                )
                db.add(new_doctor)
                imported_count += 1

        db.commit()

        return {
            "message": "Import completed successfully",
            "imported": imported_count,
            "updated": updated_count
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/admin/reset-database")
def reset_database(db: Session = Depends(get_db)):
    """
    WARNING: This will delete all data and recreate the tables.
    Should only be used in development/testing.
    """
    if os.getenv("ENVIRONMENT", "production").lower() == "production":
        raise HTTPException(
            status_code=403,
            detail="Database reset not allowed in production environment"
        )
    
    try:
        # Close all existing connections
        db.close()
        
        # Drop and recreate all tables
        models.Base.metadata.drop_all(bind=engine)
        models.Base.metadata.create_all(bind=engine)
        
        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 

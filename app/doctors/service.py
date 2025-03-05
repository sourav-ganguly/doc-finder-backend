from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import List, Optional
import json

from . import models, schemas

def get_doctors(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    specializations: Optional[List[str]] = None
) -> List[models.Doctor]:
    query = db.query(models.Doctor)
    
    if specializations:
        specialty_filters = [
            models.Doctor.speciality.ilike(f"%{spec}%") 
            for spec in specializations
        ]
        query = query.filter(or_(*specialty_filters))
    
    query = query.order_by(func.random())
    return query.offset(skip).limit(limit).all()

def create_doctor(db: Session, doctor: schemas.DoctorCreate) -> models.Doctor:
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def import_doctors(db: Session, file_path: str) -> dict:
    with open(file_path, "r") as f:
        doctors_data = json.load(f)

    imported_count = 0
    updated_count = 0

    for doctor in doctors_data:
        existing_doctor = db.query(models.Doctor).filter(
            models.Doctor.name == doctor["name"],
            models.Doctor.speciality == doctor["specialty"]
        ).first()

        if existing_doctor:
            # Update existing doctor
            for key, value in doctor.items():
                if key == "specialty":
                    setattr(existing_doctor, "speciality", value)
                elif key == "dataScrappedAt":
                    setattr(existing_doctor, "data_scrapped_at", 
                           datetime.strptime(value, "%Y-%m-%d") if value else None)
                else:
                    setattr(existing_doctor, key, value)
            updated_count += 1
        else:
            # Create new doctor
            new_doctor = models.Doctor(
                name=doctor["name"],
                title=doctor.get("title"),
                speciality=doctor["specialty"],
                educational_degree=doctor.get("educationalDegree"),
                description=doctor.get("description"),
                location=doctor.get("location"),
                data_source=doctor.get("dataSource"),
                data_scrapped_at=datetime.strptime(doctor["dataScrappedAt"], "%Y-%m-%d") 
                    if doctor.get("dataScrappedAt") else None,
                clinics=doctor.get("clinics", []),
                chambers=doctor.get("chambers", [])
            )
            db.add(new_doctor)
            imported_count += 1

    db.commit()
    return {"imported": imported_count, "updated": updated_count} 
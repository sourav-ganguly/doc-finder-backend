from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os

from ..database import get_db, engine
from ..doctors.models import Base
from ..doctors import service as doctors_service

router = APIRouter()

@router.post("/import-doctors")
def import_doctors(db: Session = Depends(get_db)):
    """Import doctors from the JSON file."""
    try:
        result = doctors_service.import_doctors(
            db=db,
            file_path="doctor_data/merged_doctors_list_v2.json"
        )
        return {
            "message": "Import completed successfully",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-database")
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
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
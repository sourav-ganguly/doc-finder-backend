from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from . import service, schemas

router = APIRouter()

@router.post("/import-doctors")
def import_doctors(
    request: schemas.ImportDoctorsRequest,
    db: Session = Depends(get_db)
):
    """
    Import doctors from the JSON file.
    
    Requires admin password for authentication.
    """
    return service.import_doctors_from_file(
        db=db,
        file_path="doctor_data/merged_doctors_list_v2.json",
        admin_password=request.admin_password
    )

@router.post("/reset-database")
def reset_database(
    request: schemas.ResetDatabaseRequest,
    db: Session = Depends(get_db)
):
    """
    WARNING: This will delete all data and recreate the tables.
    Should only be used in development/testing.
    
    Requires admin password for authentication.
    """
    return service.reset_database_tables(
        db=db,
        admin_password=request.admin_password
    ) 
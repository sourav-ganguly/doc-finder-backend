from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.decorators import admin_rate_limit
from app.database import get_db

from . import schemas, service

router = APIRouter()


@router.post("/import-doctors")
@admin_rate_limit()
def import_doctors(
    request: Request,
    form_data: schemas.ImportDoctorsRequest,
    db: Session = Depends(get_db),
):
    """
    Import doctors from the JSON file.

    Requires admin password for authentication.
    """
    return service.import_doctors_from_file(
        db=db,
        file_path="doctor_data/merged_doctors_list_v2.json",
        admin_password=form_data.admin_password,
    )


@router.post("/reset-database")
@admin_rate_limit()
def reset_database(
    request: Request,
    form_data: schemas.ResetDatabaseRequest,
    db: Session = Depends(get_db),
):
    """
    WARNING: This will delete all data and recreate the tables.
    Should only be used in development/testing.

    Requires admin password for authentication.
    """
    return service.reset_database_tables(db=db, admin_password=form_data.admin_password)

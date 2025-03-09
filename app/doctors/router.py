from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.config.decorators import doctor_rate_limit
from app.database import get_db
from app.doctors import schemas, service
from app.symptoms_matcher import match_specialization

router = APIRouter()


@router.get("/", response_model=List[schemas.Doctor])
@doctor_rate_limit()
def get_doctors(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve a randomized list of doctors with pagination support.
    Optional search parameter to filter doctors by matching specializations.
    """
    specializations = None
    if search:
        specializations = [
            spec.strip() for spec in match_specialization(search).split(";")
        ]

    doctors = service.get_doctors(
        db=db, skip=skip, limit=limit, specializations=specializations
    )
    return doctors


@router.post("/", response_model=schemas.Doctor, status_code=201)
@doctor_rate_limit()
def create_doctor(
    request: Request, doctor: schemas.DoctorCreate, db: Session = Depends(get_db)
):
    """Create a new doctor."""
    return service.create_doctor(db=db, doctor=doctor)

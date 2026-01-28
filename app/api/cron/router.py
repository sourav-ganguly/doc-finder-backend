from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.doctors import service as doctors_service
from app.database import get_db

router = APIRouter()


@router.get("/ping-doctors")
def ping_doctors(
    doctor_type: str = Query("general", alias="type"),
    db: Session = Depends(get_db),
):
    """Lightweight cron endpoint to touch the doctors table once per day."""
    specializations = [doctor_type] if doctor_type else None
    doctors = doctors_service.get_doctors(db, limit=1, specializations=specializations)
    return {
        "ok": True,
        "requested_type": doctor_type,
        "matched": len(doctors),
    }

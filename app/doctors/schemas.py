from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class DoctorBase(BaseModel):
    name: str
    title: Optional[str] = None
    speciality: str
    educational_degree: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    data_source: Optional[str] = None
    data_scrapped_at: Optional[date] = None
    clinics: Optional[List[str]] = []
    chambers: Optional[List[str]] = []

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int

    class Config:
        from_attributes = True 
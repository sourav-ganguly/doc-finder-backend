from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DocumentBase(BaseModel):
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DoctorBase(BaseModel):
    name: str
    speciality: str
    phone_number: Optional[str] = None
    location: str
    educational_degree: Optional[str] = None
    description: Optional[str] = None
    data_source: Optional[str] = None

class DoctorCreate(DoctorBase):
    data_scrapped_at: Optional[datetime] = None

class Doctor(DoctorBase):
    id: int
    data_scrapped_at: datetime

    class Config:
        from_attributes = True 
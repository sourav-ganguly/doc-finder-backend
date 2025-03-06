from sqlalchemy import ARRAY, Column, DateTime, Integer, String

from ..database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    title = Column(String)
    speciality = Column(String, index=True)
    phone_number = Column(String)
    location = Column(String)
    educational_degree = Column(String)
    description = Column(String)
    data_scrapped_at = Column(DateTime)
    data_source = Column(String)
    clinics = Column(ARRAY(String))
    chambers = Column(ARRAY(String))

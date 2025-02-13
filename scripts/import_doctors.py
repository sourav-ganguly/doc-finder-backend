import sys
import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the app directory to the Python path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Doctor, Base
from app.database import SQLALCHEMY_DATABASE_URL

def import_doctors():
    """
    Import doctors from the JSON file if they don't already exist in the database.
    """
    # Create database connection
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Read the JSON file
        with open("doctor_data/doctor-list-square-v2.json", "r") as f:
            doctors_data = json.load(f)

        imported_count = 0
        skipped_count = 0

        for doctor in doctors_data:
            # Check if doctor already exists by name and speciality
            existing_doctor = db.query(Doctor).filter(
                Doctor.name == doctor["name"],
                Doctor.speciality == doctor["specialty"]
            ).first()

            if existing_doctor:
                skipped_count += 1
                print(f"Skipped: {doctor['name']} (already exists)")
                continue

            # Create new doctor object
            new_doctor = Doctor(
                name=doctor["name"],
                speciality=doctor["specialty"],
                educational_degree=doctor.get("educationalDegree"),
                description=doctor.get("description"),
                location=doctor.get("location"),
                data_source=doctor.get("dataSource"),
                data_scrapped_at=datetime.strptime(doctor["dataScrappedAt"], "%Y-%m-%d") if doctor.get("dataScrappedAt") else None
            )

            db.add(new_doctor)
            imported_count += 1
            print(f"Imported: {doctor['name']}")

        db.commit()
        print(f"\nImport completed successfully!")
        print(f"Imported: {imported_count}")
        print(f"Skipped: {skipped_count}")

    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_doctors() 
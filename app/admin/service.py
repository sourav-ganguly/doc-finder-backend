from sqlalchemy.orm import Session
import os
from fastapi import HTTPException

from ..database import engine, Base
from ..doctors import service as doctors_service


def verify_admin_password(password: str):
    """
    Verify that the provided password matches the admin password from environment variables.
    
    Args:
        password: The password to verify
        
    Returns:
        True if password matches, raises HTTPException otherwise
    """
    admin_password = os.getenv("ADMIN_PASSWORD")
    if not admin_password:
        raise HTTPException(
            status_code=500,
            detail="Admin password not configured in environment variables"
        )
    
    if password != admin_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin password"
        )
    
    return True


def import_doctors_from_file(db: Session, file_path: str, admin_password: str):
    """
    Import doctors from a JSON file.
    
    Args:
        db: Database session
        file_path: Path to the JSON file containing doctor data
        admin_password: Admin password for authentication
        
    Returns:
        Dictionary with import results
    """
    # Verify admin password
    verify_admin_password(admin_password)
    
    try:
        result = doctors_service.import_doctors(
            db=db,
            file_path=file_path
        )
        return {
            "message": "Import completed successfully",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def reset_database_tables(db: Session, admin_password: str):
    """
    Reset the database by dropping and recreating all tables.
    
    Args:
        db: Database session
        admin_password: Admin password for authentication
        
    Returns:
        Dictionary with operation result
    """
    # Verify admin password
    verify_admin_password(admin_password)
    
    # Check environment to prevent accidental reset in production
    if os.getenv("ENVIRONMENT", "production").lower() == "production":
        raise HTTPException(
            status_code=403,
            detail="Database reset not allowed in production environment"
        )
    
    try:
        # Close the current session
        db.close()
        
        # Drop and recreate all tables
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        return {"message": "Database reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
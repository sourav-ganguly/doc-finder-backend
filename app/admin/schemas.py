from pydantic import BaseModel


class AdminAuth(BaseModel):
    """Schema for admin authentication."""
    admin_password: str


class ImportDoctorsRequest(AdminAuth):
    """Request schema for importing doctors."""


class ResetDatabaseRequest(AdminAuth):
    """Request schema for resetting database."""

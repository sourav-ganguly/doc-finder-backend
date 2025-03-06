from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from . import service

router = APIRouter()


class SpecializationRequest(BaseModel):
    query: str


class SpecializationResponse(BaseModel):
    specializations: list[str]


@router.post("/match-specialization", response_model=SpecializationResponse)
def get_matching_specialization(request: SpecializationRequest):
    """
    Match a user's health query to relevant medical specializations.
    """
    try:
        specialization_str = service.match_specialization(request.query)
        specializations = [spec.strip() for spec in specialization_str.split(";")]
        return {"specializations": specializations}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error matching specialization: {str(e)}"
        ) from e

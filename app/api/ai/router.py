from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.config.decorators import ai_rate_limit

from . import service

router = APIRouter()


class SpecializationRequest(BaseModel):
    query: str


class SpecializationResponse(BaseModel):
    specializations: list[str]


@router.get("/match-specialization", response_model=SpecializationResponse)
@ai_rate_limit()
def get_matching_specialization(request: Request, query: str):
    """
    Match a user's health query to relevant medical specializations.
    """
    try:
        specialization_str = service.match_specialization(query)
        specializations = [spec.strip() for spec in specialization_str.split(";")]
        return {"specializations": specializations}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error matching specialization: {str(e)}"
        ) from e

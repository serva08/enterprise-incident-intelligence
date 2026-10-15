from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_incident_service
from app.schemas import IncidentCreate, IncidentResponse
from app.services.incident_service import IncidentNotFoundError, IncidentService

router = APIRouter()


@router.post("", response_model=IncidentResponse, status_code=201)
def create_incident(
    incident: IncidentCreate,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    return service.create_incident(incident)


@router.get("", response_model=list[IncidentResponse])
def list_incidents(
    service: IncidentService = Depends(get_incident_service),
) -> list[IncidentResponse]:
    return service.list_incidents()


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    try:
        return service.get_incident(incident_id)
    except IncidentNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        ) from error

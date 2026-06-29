from fastapi import APIRouter, Path, Depends, HTTPException
from pydantic import BaseModel
from services.appointments import AppointmentService


router = APIRouter()


class AppointmentDeleteResponse(BaseModel):
    message: str
    appointment_id: int


@router.delete("/appointments/{id}", response_model=AppointmentDeleteResponse)
async def delete_appointment(
    id: int = Path(...), appointment_service: AppointmentService = Depends()
):
    try:
        appointment_id = appointment_service.delete_appointment(id)
        return AppointmentDeleteResponse(
            message="Appointment deleted successfully", appointment_id=appointment_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

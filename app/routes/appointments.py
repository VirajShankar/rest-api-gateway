from fastapi import APIRouter, Path, Depends, HTTPException
from pydantic import BaseModel
from app.services.appointments import AppointmentService
from main import get_appointment_service

router = APIRouter()


class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str


@router.get("/appointments/{id}", response_model=AppointmentResponse)
async def get_appointment(
    id: int = Path(..., gt=0),
    appointment_service: AppointmentService = Depends(get_appointment_service),
):
    appointment: dict = appointment_service.get_appointment(id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return AppointmentResponse(
        id=int(appointment["id"]),
        user=appointment["user"],
        time=appointment["time"],
        status=appointment["status"],
    )

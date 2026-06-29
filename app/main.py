from fastapi import FastAPI, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from db_client import Session
from services import AppointmentService

app = FastAPI()

def get_appointment_service() -> AppointmentService:
    return AppointmentService()

@app.get("/appointments/{id}")
async def get_appointment(id: int, appointment_service: AppointmentService = Depends(get_appointment_service)):
    appointment = appointment_service.get_appointment(id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

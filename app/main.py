from fastapi import FastAPI
from routes.appointments import router
from app.db_client import AppointmentDbClient
from app.services.appointments import AppointmentService

app = FastAPI()

db_client = AppointmentDbClient()
appointment_service = AppointmentService(db_client)


def get_appointment_service() -> AppointmentService:
    return appointment_service


app.include_router(router)

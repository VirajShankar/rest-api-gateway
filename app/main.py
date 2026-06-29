from fastapi import FastAPI
from routes.appointments import router
from db_client.appointments import AppointmentDbClient
from services.appointments import AppointmentService

app = FastAPI()

db_client = AppointmentDbClient()
appointment_service = AppointmentService(db_client)


def get_appointment_service():
    return appointment_service


app.include_router(router)

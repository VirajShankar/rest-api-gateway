from fastapi import Depends
from pydantic import BaseModel
from db_client.appointment_db_client import AppointmentDBClient
from db_client.error_format import default_appointment_not_found_response

class Appointment(BaseModel):
    id: int
    user: str
    time: str
    status: str

class AppointmentService:
    def __init__(self, db_client: AppointmentDBClient):
        self.db_client = db_client

    def get_appointment(self, appointment_id: int):
        try:
            query = "SELECT * FROM appointments WHERE id = ?"
            self.db_client.cursor.execute(query, (appointment_id,))
            appointment = self.db_client.cursor.fetchone()
            if appointment is None:
                return {"error": default_appointment_not_found_response["detail"], "status_code": 404}
            else:
                return Appointment(**appointment)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

def get_appointment_service(db_client: AppointmentDBClient = Depends(get_db)):
    return AppointmentService(db_client)


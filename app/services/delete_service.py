from fastapi import Depends
from pydantic import BaseModel
from db_client.appointment_db_client import AppointmentDBClient
from db_client.error_format import default_error_response
from db_client.error_format import default_appointment_not_found_response

class DeleteAppointmentResponse(BaseModel):
    id: int

class DeleteService:
    def __init__(self, db_client: AppointmentDBClient):
        self.db_client = db_client

    def delete_appointment(self, appointment_id: int):
        try:
            if not self.db_client.check_appointment_exists(appointment_id):
                return {"error": default_appointment_not_found_response["detail"], "status_code": 404}
            else:
                deleted_count = self.db_client.delete_appointment(appointment_id)
                if deleted_count == 1:
                    return None
                else:
                    return {"error": "Internal Server Error", "status_code": 500}
        except Exception as e:
            return {"error": str(e)}

def get_delete_service(db_client: AppointmentDBClient = Depends(get_db)):
    return DeleteService(db_client)


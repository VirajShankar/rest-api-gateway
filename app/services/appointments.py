from db_client.appointments import AppointmentDbClient


class AppointmentService:
    def __init__(self, db_client: AppointmentDbClient):
        self.db_client = db_client

    def delete_appointment(self, id: int) -> int:
        return self.db_client.delete_appointment(id)

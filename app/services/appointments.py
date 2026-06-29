from app import db_client


class AppointmentService:
    def __init__(self, db_client: db_client.AppointmentDbClient):
        self.db_client = db_client

    def get_appointment(self, id: int):
        return self.db_client.get_appointment(id)

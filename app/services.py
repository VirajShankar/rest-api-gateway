from typing import Optional
from db_client import Session
from models import Appointment

class AppointmentService:
    def __init__(self, db: Session = None):
        self.db = db

    def get_appointment(self, id: int) -> Optional[Appointment]:
        return self.db.query(Appointment).get(id)

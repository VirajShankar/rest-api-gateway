import requests
from typing import Any


class AppointmentDbClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    def delete_appointment(self, id: int) -> int:
        url: str = f"{self.base_url}/appointments/{id}"
        response: Any = requests.delete(url)
        if response.status_code == 404:
            raise ValueError("Appointment not found")
        if response.status_code != 204:
            raise Exception("Failed to delete appointment")
        return id

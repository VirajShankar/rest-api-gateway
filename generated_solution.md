### FILE: main.py
```python
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

```

### FILE: db_client/appointments.py
```python
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

```

### FILE: routes/appointments.py
```python
from fastapi import APIRouter, Path, Depends, HTTPException
from pydantic import BaseModel
from services.appointments import AppointmentService


router = APIRouter()


class AppointmentDeleteResponse(BaseModel):
    message: str
    appointment_id: int


@router.delete("/appointments/{id}", response_model=AppointmentDeleteResponse)
async def delete_appointment(
    id: int = Path(...), appointment_service: AppointmentService = Depends()
):
    try:
        appointment_id = appointment_service.delete_appointment(id)
        return AppointmentDeleteResponse(
            message="Appointment deleted successfully", appointment_id=appointment_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

```

### FILE: services/appointments.py
```python
from db_client.appointments import AppointmentDbClient


class AppointmentService:
    def __init__(self, db_client: AppointmentDbClient):
        self.db_client = db_client

    def delete_appointment(self, id: int) -> int:
        return self.db_client.delete_appointment(id)

```
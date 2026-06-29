### FILE: main.py
```python
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

```

### FILE: app/services/appointments.py
```python
from app import db_client
from typing import Dict, Any


class AppointmentService:
    def __init__(self, db_client: db_client.AppointmentDbClient):
        self.db_client = db_client

    def get_appointment(self, id: int) -> Dict[str, Any]:
        return self.db_client.get_appointment(id)

```

### FILE: routes/appointments.py
```python
from fastapi import APIRouter, Path, Depends, HTTPException
from pydantic import BaseModel
from app.services.appointments import AppointmentService
from main import get_appointment_service

router = APIRouter()


class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str


@router.get("/appointments/{id}", response_model=AppointmentResponse)
async def get_appointment(
    id: int = Path(..., gt=0),
    appointment_service: AppointmentService = Depends(get_appointment_service),
):
    appointment: dict = appointment_service.get_appointment(id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return AppointmentResponse(
        id=int(appointment["id"]),
        user=appointment["user"],
        time=appointment["time"],
        status=appointment["status"],
    )

```
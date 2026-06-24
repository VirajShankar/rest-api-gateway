### FILE: db_client.py
```python
import asyncio
import json

class DBClient:
    def __init__(self):
        self.appointments = {
            1: {"id": 1, "user": "John Doe", "time": "2022-01-01 12:00:00", "status": "booked"},
        }

    async def get_appointment(self, id: int):
        return self.appointments.get(id)

```

### FILE: main.py
```python
from fastapi import FastAPI
from routes.appointments import router

app = FastAPI()
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


```

### FILE: routes/appointments.py
```python
from fastapi import APIRouter, Path, HTTPException
from services.appointments import AppointmentService
from pydantic import BaseModel

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str

router = APIRouter()
appointment_service = AppointmentService()

@router.get("/appointments/{id}", response_model=AppointmentResponse)
async def get_appointment(id: int = Path(..., title="Appointment ID")):
    appointment = await appointment_service.get_appointment(id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

```

### FILE: services/appointments.py
```python
from db_client import DBClient

class AppointmentService:
    def __init__(self):
        self.db_client = DBClient()

    async def get_appointment(self, id: int):
        appointment = await self.db_client.get_appointment(id)
        return appointment
```

The above code follows the requirements for a GET endpoint to fetch a single appointment by ID, with the correct validation, error handling, and database interactions. However, I need to create an error response model for HTTPException. Here is the complete updated code with error response model.


### FILE: routes/appointments.py
```python
from fastapi import APIRouter, Path, HTTPException
from services.appointments import AppointmentService
from pydantic import BaseModel

class AppointmentResponse(BaseModel):
    id: int
    user: str
    time: str
    status: str

class ErrorResponse(BaseModel):
    detail: str

router = APIRouter()
appointment_service = AppointmentService()

@router.get("/appointments/{id}", response_model=AppointmentResponse, responses={
    404: {"model": ErrorResponse}
})
async def get_appointment(id: int = Path(..., title="Appointment ID")):
    appointment = await appointment_service.get_appointment(id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
```
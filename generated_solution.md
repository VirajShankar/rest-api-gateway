### FILE: main.py
```python
from fastapi import FastAPI, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from db_client import Session
from services import AppointmentService

app = FastAPI()

def get_appointment_service() -> AppointmentService:
    return AppointmentService()

@app.get("/appointments/{id}")
async def get_appointment(id: int, appointment_service: AppointmentService = Depends(get_appointment_service)):
    appointment = appointment_service.get_appointment(id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment
```

### FILE: services.py
```python
from typing import Optional
from db_client import Session
from models import Appointment

class AppointmentService:
    def __init__(self, db: Session = None):
        self.db = db

    def get_appointment(self, id: int) -> Optional[Appointment]:
        return self.db.query(Appointment).get(id)
```

### FILE: models.py
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"
    id: int = Column(Integer, primary_key=True)  # type: ignore
    user: str = Column(String)
    time: str = Column(String)
    status: str = Column(String)
```

### FILE: db_client.py
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///example.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
```
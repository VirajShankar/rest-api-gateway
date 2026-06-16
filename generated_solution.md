### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.graphql_client import run_query

router = APIRouter(prefix="/appointments", tags=["Appointments"])


class CreateAppointmentRequest(BaseModel):
    user: str
    time: str


class UpdateAppointmentRequest(BaseModel):
    time: str


@router.get("/")
def get_appointments():
    data = run_query("""
        query {
            appointments {
                id
                user
                time
                status
            }
        }
    """)
    return data.get("appointments", [])


@router.get("/{appointment_id}")
def get_appointment(appointment_id: int):
    data = run_query(
        """
        query GetAppointment($id: Int!) {
            appointment(id: $id) {
                id
                user
                time
                status
            }
        }
        """,
        variables={"id": appointment_id},
    )
    result = data.get("appointment")
    if result is None:
        raise HTTPException(status_code=404, detail={"error": "Appointment not found"})
    return result


@router.post("/")
def create_appointment(req: CreateAppointmentRequest):
    data = run_query(
        """
        mutation CreateAppointment($user: String!, $time: String!) {
            createAppointment(input: { user: $user, time: $time }) {
                id
                user
                time
                status
            }
        }
        """,
        variables={"user": req.user, "time": req.time},
    )
    return data.get("createAppointment")


@router.put("/{appointment_id}")
def update_appointment(appointment_id: int, req: UpdateAppointmentRequest):
    data = run_query(
        """
        mutation UpdateAppointment($id: Int!, $time: String!) {
            updateAppointment(id: $id, input: { time: $time }) {
                id
                user
                time
                status
            }
        }
        """,
        variables={"id": appointment_id, "time": req.time},
    )
    return data.get("updateAppointment")


@router.delete("/{appointment_id}")
def cancel_appointment(appointment_id: int):
    data = run_query(
        """
        mutation CancelAppointment($id: Int!) {
            cancelAppointment(id: $id)
        }
        """,
        variables={"id": appointment_id},
    )
    return {"cancelled": data.get("cancelAppointment")}


@router.get("/search")
def search_appointments(user: str = Query(None), time: str = Query(None)):
    if user is None and time is None:
        raise HTTPException(status_code=400, detail={"error": "At least one query parameter is required"})

    query = """
        query SearchAppointments($user: String, $time: String) {
            appointments(user: $user, time: $time) {
                id
                user
                time
                status
            }
        }
    """
    variables = {}
    if user:
        variables["user"] = user
    if time:
        variables["time"] = time

    data = run_query(query, variables)
    return data.get("appointments", [])

```
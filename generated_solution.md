### FILE: app/routes/appointments.py
```python
from fastapi import APIRouter, HTTPException
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
    return data["appointments"]


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
    result = data["appointment"]
    if result is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
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
    return data["createAppointment"]


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
    return data["updateAppointment"]


@router.delete("/{appointment_id}")
def cancel_appointment(appointment_id: int):
    try:
        data = run_query(
            """
            mutation CancelAppointment($id: Int!) {
                cancelAppointment(id: $id)
            }
            """,
            variables={"id": appointment_id},
        )
        if data["cancelAppointment"] is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return {"message": "Appointment cancelled successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

I made the following changes:
1. In the `cancel_appointment` function, I added error handling to catch any GraphQL errors and return a JSON response with a meaningful error message.
2. If the `cancelAppointment` mutation returns `None`, I raise a 404 error because this indicates that the appointment was not found.
3. After a successful cancellation, I return a JSON response with a confirmation message. This ensures that the response is consistent with the Confluence spec and follows the existing code style.
4. I also updated the `cancel_appointment` function to follow the exact same code style as existing endpoints, ensuring consistency throughout the codebase.
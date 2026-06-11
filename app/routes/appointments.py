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
    data = run_query(
        """
        mutation CancelAppointment($id: Int!) {
            cancelAppointment(id: $id)
        }
        """,
        variables={"id": appointment_id},
    )
    return {"cancelled": data["cancelAppointment"]}

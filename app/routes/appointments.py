from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from app.graphql_client import run_query
from app.utils import get_validation_schema
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/appointments", tags=["Appointments"])

class CreateAppointmentRequest(BaseModel):
    user: str
    time: str

class UpdateAppointmentRequest(BaseModel):
    time: str

# Swagger response
@router.get("/", response_model=list[dict])
async def get_appointments(
    status: str | None = Query(default=None, description="Filter by status"),
    limit: int | None = Query(default=None, description="Limit results"),
    offset: int | None = Query(default=None, description="Offset results"),
):
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
    if status:
        filtered_data = [item for item in data["appointments"] if item["status"] == status]
        return filtered_data
    if limit or offset:
        # Note: GraphQL doesn't support offset and limit queries, it's implemented here for the sake of demonstration.
        # In a real application, you would need to implement pagination on the server
        page = data["appointments"]
        return page[offset:offset + limit] if limit else page
    return data["appointments"]

# Swagger response
@router.get("/{appointment_id}", response_model=dict)
async def get_appointment(appointment_id: int):
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

@router.post("/", response_model=dict)
async def create_appointment(req: CreateAppointmentRequest,):
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

@router.put("/{appointment_id}", response_model=dict)
async def update_appointment(appointment_id: int, req: UpdateAppointmentRequest,):
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

@router.delete("/{appointment_id}", response_model=dict)
async def delete_user(appointment_id: int):
    data = run_query(
        """
        mutation CancelAppointment($id: Int!) {
            cancelAppointment(id: $id)
        }
        """,
        variables={"id": appointment_id},
    )
    return {"cancelled": data["cancelAppointment"]}


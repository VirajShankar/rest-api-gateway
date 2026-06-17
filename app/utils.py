from pydantic import BaseModel

def get_validation_schema(endpoint: str) -> BaseModel:
    # Map API endpoints to validation schemas
    endpoint_mapping = {
        "appointments": {
            "get_appointments": CreateAppointmentQueryParams,
            "get_appointment": GetAppointmentQueryParams,
            "create_appointment": CreateAppointmentRequest,
            "update_appointment": UpdateAppointmentRequest,
            "cancel_appointment": CancelAppointmentQueryParams,
        },
    }
    # Extract endpoint and method
    endpoint_parts = endpoint.split("/")
    endpoint_method = endpoint_parts[-1]
    endpoint_name = "/".join(endpoint_parts[:-1])

    return endpoint_mapping[endpoint_name][endpoint_method]

# Swagger query parameters
class CreateAppointmentQueryParams(BaseModel):
    status: str | None = Query(default=None, description="Filter by status")
    limit: int | None = Query(default=None, description="Limit results")
    offset: int | None = Query(default=None, description="Offset results")

class GetAppointmentQueryParams(BaseModel):
    pass

class CancelAppointmentQueryParams(BaseModel):
    pass


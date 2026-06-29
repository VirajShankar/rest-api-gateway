import requests


class AppointmentDbClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url

    def get_appointment(self, id: int):
        response = requests.get(
            f"{self.base_url}/graphql",
            headers={"Content-Type": "application/json"},
            json={
                "query": """
                    query GetAppointment($id: Int!){
                      appointment(id: $id){
                        id
                        user
                        time
                        status
                      }
                    }
                """,
                "variables": {"id": id},
            },
        )
        if response.status_code != 200:
            return None
        data = response.json()
        if data.get("errors") is not None:
            return None
        appointment = data.get("data", {}).get("appointment")
        if appointment is None:
            return None
        return appointment

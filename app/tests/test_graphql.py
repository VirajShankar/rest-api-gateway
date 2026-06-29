from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_appointment():
    id = 1
    response = client.get(f"/appointments/{id}")
    assert response.status_code == 200
    assert response.json().get("id") == id


def test_get_appointment_not_found():
    id = 999
    response = client.get(f"/appointments/{id}")
    assert response.status_code == 404
    assert response.json().get("detail") == "Appointment not found"

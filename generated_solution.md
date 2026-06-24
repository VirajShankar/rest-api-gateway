### FILE: main.py
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import os
import httpx
from typing import Dict

app = FastAPI()

DATAGRAPH_URL = os.environ.get("DATAGRAPH_URL")

def run_query(query: str, variables: Dict = {}) -> JSONResponse:
    url = DATAGRAPH_URL or ""  # Ensure we have a valid URL
    response = httpx.post(url, json={"query": query, "variables": variables})
    if response.status_code == 200:
        return JSONResponse(content=response.json(), status_code=200)
    else:
        return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

@app.get("/appointments/{id}")
async def get_appointment(id: int) -> JSONResponse:
    query = """
        query GetAppointment($id: Int!) {
            appointment(id: $id) {
                id
                user
                time
                status
            }
        }
    """
    variables = {"id": id}
    response = run_query(query, variables)
    data = response.body
    if "errors" in data:
        return JSONResponse(content={"detail": "Appointment not found"}, status_code=404)
    return response
```
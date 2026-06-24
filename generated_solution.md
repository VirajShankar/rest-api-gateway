### FILE: main.py
```python
from fastapi import FastAPI, HTTPException
import httpx
from typing import Optional

app = FastAPI()

DATAGRAPH_URL = "http://localhost:5000"

def run_query(query: str) -> dict:
    response = httpx.post(DATAGRAPH_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=400, detail="Invalid query")

@app.get("/appointments/{appointment_id}")
async def get_appointment(appointment_id: int):
    query = f"""
        query {{
            appointment(id: {appointment_id}) {{
                id
                user
                time
                status
            }}
        }}
    """
    result = run_query(query)
    if "data" in result and "appointment" in result["data"]:
        appointment = result["data"]["appointment"]
        return {
            "id": appointment["id"],
            "user": appointment["user"],
            "time": appointment["time"],
            "status": appointment["status"]
        }
    else:
        raise HTTPException(status_code=404, detail="Appointment not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### FILE: requirements.txt
```
fastapi
httpx
uvicorn
```

### FILE: .env
```
DATAGRAPH_URL="http://localhost:5000"
```
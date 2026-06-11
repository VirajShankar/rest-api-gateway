from fastapi import FastAPI
from app.routes import appointments

app = FastAPI(title="REST API Gateway")

app.include_router(appointments.router)

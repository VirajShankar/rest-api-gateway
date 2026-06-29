from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"
    id: int = Column(Integer, primary_key=True)  # type: ignore
    user: str = Column(String)
    time: str = Column(String)
    status: str = Column(String)

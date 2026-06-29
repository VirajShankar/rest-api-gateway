from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base: type = declarative_base()


class AppointmentStorage(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)  # type: ignore
    user = Column(String)  # type: ignore
    time = Column(String)  # type: ignore
    status = Column(String)  # type: ignore

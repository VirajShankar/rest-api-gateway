import graphene
from sqlalchemy.orm import Session
from app.models import AppointmentStorage


class AppointmentStorageType(graphene.ObjectType):
    id = graphene.ID()
    user = graphene.String()
    time = graphene.String()
    status = graphene.String()


class Query(graphene.ObjectType):
    appointment_record = graphene.Field(
        AppointmentStorageType, id=graphene.ID(), required=True
    )

    def resolve_appointment_record(self, info, id: int) -> AppointmentStorageType:
        db_session: Session = info.context.get("db_session")
        appointment_storage: AppointmentStorage = (
            db_session.query(AppointmentStorage).filter_by(id=id).first()
        )
        if appointment_storage is None:
            return None
        return AppointmentStorageType(
            id=appointment_storage.id,
            user=appointment_storage.user,
            time=appointment_storage.time,
            status=appointment_storage.status,
        )


class AppointmentType(graphene.ObjectType):
    id = graphene.ID()
    user = graphene.String()
    time = graphene.String()
    status = graphene.String()


class AppointmentQuery(graphene.ObjectType):
    appointment = graphene.Field(AppointmentType, id=graphene.ID(), required=True)

    def resolve_appointment(self, info, id: int) -> AppointmentType:
        db_session: Session = info.context.get("db_session")
        appointment_storage: AppointmentStorage = (
            db_session.query(AppointmentStorage).filter_by(id=id).first()
        )
        if appointment_storage is None:
            return None
        return AppointmentType(
            id=appointment_storage.id,
            user=appointment_storage.user,
            time=appointment_storage.time,
            status=appointment_storage.status,
        )


schema = graphene.Schema(query=AppointmentQuery)

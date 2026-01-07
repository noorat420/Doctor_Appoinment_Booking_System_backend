# Appointment Repository - Database operations for Appointment model
from extensions import db
from models.appointment import Appointment


class AppointmentRepository:
    @staticmethod
    def get_by_id(appointment_id: int) -> Appointment | None:
        return db.session.get(Appointment, appointment_id)

    @staticmethod
    def get_by_slot_id(slot_id: int) -> Appointment | None:
        return Appointment.query.filter_by(slot_id=slot_id).first()

    @staticmethod
    def get_by_patient(patient_id: int) -> list[Appointment]:
        return (
            Appointment.query
            .filter_by(patient_id=patient_id)
            .order_by(Appointment.created_at.desc())
            .all()
        )

    @staticmethod
    def get_by_doctor(doctor_id: int) -> list[Appointment]:
        return (
            Appointment.query
            .filter_by(doctor_id=doctor_id)
            .order_by(Appointment.created_at.desc())
            .all()
        )

    @staticmethod
    def create(doctor_id: int, patient_id: int, slot_id: int) -> Appointment:
        appointment = Appointment(
            doctor_id=doctor_id,
            patient_id=patient_id,
            slot_id=slot_id
        )
        db.session.add(appointment)
        return appointment

    @staticmethod
    def delete(appointment: Appointment) -> None:
        db.session.delete(appointment)

    @staticmethod
    def cancel(appointment: Appointment) -> None:
        appointment.status = "cancelled"

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def rollback():
        db.session.rollback()

    @staticmethod
    def flush():
        db.session.flush()


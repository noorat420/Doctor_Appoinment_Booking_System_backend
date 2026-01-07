# Availability Repository - Database operations for AvailabilitySlot model
from datetime import date, time
from extensions import db
from models.availability import AvailabilitySlot


class AvailabilityRepository:
    @staticmethod
    def get_by_id(slot_id: int) -> AvailabilitySlot | None:
        return db.session.get(AvailabilitySlot, slot_id)

    @staticmethod
    def get_by_id_for_update(slot_id: int) -> AvailabilitySlot | None:
        return AvailabilitySlot.query.filter_by(id=slot_id).with_for_update().first()

    @staticmethod
    def get_available_slots(doctor_id: int) -> list[AvailabilitySlot]:
        return (
            AvailabilitySlot.query
            .filter_by(doctor_id=doctor_id, is_booked=False)
            .order_by(AvailabilitySlot.date, AvailabilitySlot.start_time)
            .all()
        )

    @staticmethod
    def create(doctor_id: int, slot_date: date, start_time: time, end_time: time) -> AvailabilitySlot:
        slot = AvailabilitySlot(
            doctor_id=doctor_id,
            date=slot_date,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(slot)
        db.session.commit()
        return slot

    @staticmethod
    def mark_as_booked(slot: AvailabilitySlot) -> None:
        slot.is_booked = True

    @staticmethod
    def mark_as_available(slot: AvailabilitySlot) -> None:
        slot.is_booked = False

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def flush():
        db.session.flush()


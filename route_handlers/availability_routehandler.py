# Availability Controller - Business logic for availability slots
from datetime import datetime

from repositories.doctor_repository import DoctorRepository
from repositories.availability_repository import AvailabilityRepository


class AvailabilityController:
    @staticmethod
    def create_slot(user_id: int, date_str: str, start_time_str: str, end_time_str: str):
      
        if not all([date_str, start_time_str, end_time_str]):
            return {"error": "Date, start time and end time are required"}, 400

        try:
            slot_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return {"error": "Invalid date or time format"}, 400

       
        if start_time >= end_time:
            return {"error": "End time must be after start time"}, 400

      
        doctor = DoctorRepository.get_by_user_id(user_id)
        if not doctor:
            return {"error": "Doctor profile not found"}, 404

        # Create slot
        slot = AvailabilityRepository.create(
            doctor_id=doctor.id,
            slot_date=slot_date,
            start_time=start_time,
            end_time=end_time
        )

        return {
            "message": "Availability slot created successfully",
            "slot_id": slot.id
        }, 201


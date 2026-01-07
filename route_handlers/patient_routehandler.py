# Patient Controller - Business logic for patient operations
from repositories.doctor_repository import DoctorRepository
from repositories.availability_repository import AvailabilityRepository


class PatientController:
    @staticmethod
    def get_dashboard():
        return {"message": "Welcome Patient"}, 200

    @staticmethod
    def list_doctors(page: int, limit: int):
        pagination = DoctorRepository.get_all_paginated(page, limit)

        doctors = [
            {
                "id": doctor.id,
                "name": doctor.user.name,
                "designation": doctor.designation,
                "specialization": doctor.specialization
            }
            for doctor in pagination.items
        ]

        return {
            "data": doctors,
            "page": page,
            "total_pages": pagination.pages,
            "total": pagination.total
        }, 200

    @staticmethod
    def get_doctor_availability(doctor_id: int):
        slots = AvailabilityRepository.get_available_slots(doctor_id)

        return {
            "data": [
                {
                    "slot_id": slot.id,
                    "date": slot.date.isoformat(),
                    "start_time": slot.start_time.strftime("%H:%M"),
                    "end_time": slot.end_time.strftime("%H:%M")
                }
                for slot in slots
            ]
        }, 200


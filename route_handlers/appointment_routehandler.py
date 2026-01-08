# Appointment Controller - Business logic for appointments
from repositories.user_repository import UserRepository
from repositories.doctor_repository import DoctorRepository  
from repositories.availability_repository import AvailabilityRepository
from repositories.appointment_repository import AppointmentRepository
from services.email_service import (
    send_appointment_confirmation,
    send_appointment_cancellation
)


class AppointmentController:
    @staticmethod
    def book_appointment(patient_id: int, slot_id: int):
        if not slot_id:
            return {"error": "slot_id is required"}, 400

        try:
            # Get slot with lock
            slot = AvailabilityRepository.get_by_id_for_update(slot_id)

            if not slot:
                return {"error": "Slot not found"}, 404

            if slot.is_booked:
                return {"error": "Slot already booked"}, 409

            # Check for existing appointment
            existing = AppointmentRepository.get_by_slot_id(slot_id)
            if existing:
                if existing.status == 'cancelled':
                    AppointmentRepository.delete(existing)
                    AppointmentRepository.flush()
                else:
                    AvailabilityRepository.mark_as_booked(slot)
                    AppointmentRepository.commit()
                    return {"error": "Slot already booked"}, 409

            # Create appointment
            appointment = AppointmentRepository.create(
                doctor_id=slot.doctor_id,
                patient_id=patient_id,
                slot_id=slot.id
            )
            AvailabilityRepository.mark_as_booked(slot)
            AppointmentRepository.commit()

        except Exception as e:
            AppointmentRepository.rollback()
            import traceback
            traceback.print_exc()
            return {"error": f"Booking failed: {str(e)}"}, 500

        # Send confirmation email
        try:
            patient = UserRepository.get_by_id(patient_id)
            doctor = DoctorRepository.get_by_id(slot.doctor_id)

            send_appointment_confirmation(
                to_email=patient.email,
                doctor_name=doctor.user.name,
                doctor_specialization=doctor.specialization,
                date=slot.date.isoformat(),
                start_time=slot.start_time.strftime("%H:%M"),
                end_time=slot.end_time.strftime("%H:%M")
            )
        except Exception as e:
            print(f"Email error: {e}")

        return {
            "message": "Appointment booked successfully",
            "appointment_id": appointment.id
        }, 201

    @staticmethod
    def get_patient_appointments(patient_id: int):
        appointments = AppointmentRepository.get_by_patient(patient_id)

        data = [
            {
                "appointment_id": appt.id,
                "doctor_name": appt.doctor.user.name,
                "date": appt.slot.date.isoformat(),
                "start_time": appt.slot.start_time.strftime("%H:%M"),
                "end_time": appt.slot.end_time.strftime("%H:%M"),
                "status": appt.status
            }
            for appt in appointments
        ]

        return {"data": data}, 200

    @staticmethod
    def get_doctor_appointments(user_id: int):
        doctor = DoctorRepository.get_by_user_id(user_id)

        if not doctor:
            return {"error": "Doctor profile not found"}, 404

        appointments = AppointmentRepository.get_by_doctor(doctor.id)

        data = [
            {
                "appointment_id": appt.id,
                "patient_name": appt.patient.name,
                "date": appt.slot.date.isoformat(),
                "start_time": appt.slot.start_time.strftime("%H:%M"),
                "end_time": appt.slot.end_time.strftime("%H:%M"),
                "status": appt.status
            }
            for appt in appointments
        ]

        return {"data": data}, 200

    @staticmethod
    def cancel_appointment(appointment_id: int, user_id: int, role: str):
        appointment = AppointmentRepository.get_by_id(appointment_id)

        if not appointment:
            return {"error": "Appointment not found"}, 404

    
        if role == "patient":
            if appointment.patient_id != user_id:
                return {"error": "Access denied"}, 403
        elif role == "doctor":
            doctor = DoctorRepository.get_by_user_id(user_id)
            if not doctor or appointment.doctor_id != doctor.id:
                return {"error": "Access denied"}, 403
        else:
            return {"error": "Invalid role"}, 403

        if appointment.status == "cancelled":
            return {"error": "Appointment already cancelled"}, 409

       
        AppointmentRepository.cancel(appointment)
        AvailabilityRepository.mark_as_available(appointment.slot)
        AppointmentRepository.commit()

     
        try:
            patient = UserRepository.get_by_id(appointment.patient_id)
            doctor = DoctorRepository.get_by_id(appointment.doctor_id)
            cancelled_by = "Doctor" if role == "doctor" else "Patient"

            # Email to patient
            send_appointment_cancellation(
                to_email=patient.email,
                recipient_name=patient.name,
                doctor_name=doctor.user.name,
                doctor_specialization=doctor.specialization,
                date=appointment.slot.date.isoformat(),
                start_time=appointment.slot.start_time.strftime("%H:%M"),
                end_time=appointment.slot.end_time.strftime("%H:%M"),
                cancelled_by=cancelled_by
            )

            # Email to doctor
            send_appointment_cancellation(
                to_email=doctor.user.email,
                recipient_name=doctor.user.name,
                doctor_name=doctor.user.name,
                doctor_specialization=doctor.specialization,
                date=appointment.slot.date.isoformat(),
                start_time=appointment.slot.start_time.strftime("%H:%M"),
                end_time=appointment.slot.end_time.strftime("%H:%M"),
                cancelled_by=cancelled_by
            )
        except Exception as e:
            print(f"Cancellation email error: {e}")

        return {"message": "Appointment cancelled successfully"}, 200


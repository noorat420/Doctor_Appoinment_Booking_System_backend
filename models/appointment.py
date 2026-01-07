# Appointment model
from datetime import datetime
from extensions import db

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    slot_id = db.Column(
        db.Integer,
        db.ForeignKey("availability_slots.id"),
        nullable=False,
        unique=True
    )

    status = db.Column(db.String(20), default="booked")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("Doctor")
    patient = db.relationship("User")
    slot = db.relationship("AvailabilitySlot")

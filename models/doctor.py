# Doctor model
from extensions import db

class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    designation = db.Column(db.String(50))
    specialization = db.Column(db.String(100))

    user = db.relationship("User", backref="doctor_profile")
    availability_slots = db.relationship('AvailabilitySlot', backref='doctor', cascade='all, delete-orphan')
    appointments = db.relationship(
        'Appointment',
        backref='doctor',
        cascade='all, delete-orphan',
        lazy=True
    )

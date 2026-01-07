# Doctor Repository - Database operations for Doctor model
from extensions import db
from models.user import User
from models.doctor import Doctor


class DoctorRepository:
    @staticmethod
    def get_by_id(doctor_id: int) -> Doctor | None:
        return db.session.get(Doctor, doctor_id)

    @staticmethod
    def get_by_user_id(user_id: int) -> Doctor | None:
        return Doctor.query.filter_by(user_id=user_id).first()

    @staticmethod
    def create(user_id: int, designation: str = None, specialization: str = None) -> Doctor:
        doctor = Doctor(
            user_id=user_id,
            designation=designation,
            specialization=specialization
        )
        db.session.add(doctor)
        db.session.commit()
        return doctor

    @staticmethod
    def get_all_paginated(page: int, limit: int):
        query = Doctor.query.join(User)
        return query.paginate(page=page, per_page=limit, error_out=False)

    @staticmethod
    def create_or_update(user_id: int, designation: str = None, specialization: str = None) -> Doctor:
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if not doctor:
            doctor = Doctor(
                user_id=user_id,
                designation=designation,
                specialization=specialization
            )
            db.session.add(doctor)
        else:
            if designation is not None:
                doctor.designation = designation
            if specialization is not None:
                doctor.specialization = specialization
        db.session.commit()
        return doctor

    @staticmethod
    def delete_by_user_id(user_id: int) -> bool:
        doctor = Doctor.query.filter_by(user_id=user_id).first()
        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            return True
        return False
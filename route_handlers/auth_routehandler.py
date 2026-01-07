# Auth Controller - Business logic for authentication
from flask import current_app
from flask_jwt_extended import create_access_token
from repositories.user_repository import UserRepository
from repositories.doctor_repository import DoctorRepository
from utils.security import hash_password, verify_password


class AuthController:

    @staticmethod
    def register(name: str, email: str, password: str, role: str, invitation_code: str = None):
      
        if not all([name, email, password, role]):
            return {"error": "All fields are required"}, 400

        if role not in ["doctor", "patient"]:
            return {"error": "Invalid role"}, 400

    
        if role == "doctor":
            if not invitation_code:
                return {"error": "Invitation code is required"}, 400

            valid_code = current_app.config.get(
                "DOCTOR_INVITATION_CODE", "DOC2024SECRET"
            )

            if invitation_code != valid_code:
                return {"error": "Invitation code is invalid"}, 403

    
        if UserRepository.email_exists(email):
            return {"error": "User already exists with this email"}, 409

        # Create user
        user = UserRepository.create(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role
        )

        # Create doctor profile
        if role == "doctor":
            DoctorRepository.create(
                user_id=user.id,
                designation="Dr.",
                specialization="General Practitioner"
            )

        return {"message": "User registered successfully"}, 201

    @staticmethod
    def login(email: str, password: str):
        if not email or not password:
            return {"error": "Email and password are required"}, 400

        user = UserRepository.get_by_email(email)

     
        if not user:
            return {"error": "User does not exist"}, 404

   
        if not verify_password(user.password_hash, password):
            return {"error": "Incorrect password"}, 401

        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role}
        )

        return {"access_token": token}, 200

    @staticmethod
    def get_current_user(user_id: int):
        user = UserRepository.get_by_id(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }, 200

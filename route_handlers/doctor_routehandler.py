# Doctor Controller - Business logic for doctor operations
from repositories.doctor_repository import DoctorRepository
from repositories.user_repository import UserRepository



class DoctorController:
    @staticmethod
    def get_dashboard():
        return {"message": "Welcome Doctor"}, 200

    @staticmethod
    def get_profile(user_id: int):
        user = UserRepository.get_by_id(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        doctor = DoctorRepository.get_by_user_id(user_id)
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "designation": doctor.designation if doctor else None,
            "specialization": doctor.specialization if doctor else None
        }, 200

    @staticmethod
    def update_profile(user_id: int, designation: str = None, specialization: str = None):
        doctor = DoctorRepository.create_or_update(
            user_id=user_id,
            designation=designation,
            specialization=specialization
        )
        return {
            "message": "Profile updated successfully",
            "designation": doctor.designation,
            "specialization": doctor.specialization
        }, 200

    @staticmethod
    def delete_account(user_id: int):
      
        DoctorRepository.delete_by_user_id(user_id)
        deleted = UserRepository.delete(user_id)
        
        if deleted:
            return {"message": "Account deleted successfully"}, 200
        return {"error": "Failed to delete account"}, 500

# User Repository - Database operations for User model
from extensions import db
from models.user import User


class UserRepository:
    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)

    @staticmethod
    def get_by_email(email: str) -> User | None:
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(name: str, email: str, password_hash: str, role: str) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def email_exists(email: str) -> bool:
        return User.query.filter_by(email=email).first() is not None

    @staticmethod
    def delete(user_id: int) -> bool:
        user = db.session.get(User, user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False


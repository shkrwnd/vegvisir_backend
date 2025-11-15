from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_student_id(self, student_id: str) -> Optional[User]:
        """Get user by student ID."""
        return self.db.query(User).filter(User.student_id == student_id).first()

    def get_by_reset_token(self, reset_token: str) -> Optional[User]:
        """Get user by reset token."""
        return self.db.query(User).filter(User.reset_token == reset_token).first()

    def create(self, user_data: UserCreate, hashed_password: str) -> User:
        """Create a new user."""
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            student_id=user_data.student_id,
            major=user_data.major,
            class_year=user_data.class_year,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user: User, **kwargs) -> User:
        """Update user fields."""
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Delete a user."""
        self.db.delete(user)
        self.db.commit()


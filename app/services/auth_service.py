from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.exceptions import UnauthorizedError, ValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password."""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def register(self, user_data: UserCreate) -> tuple[dict, str]:
        """Register a new user."""
        # Check if user already exists
        if self.user_repo.get_by_email(user_data.email):
            raise ValidationError("Email already registered")
        
        if user_data.student_id and self.user_repo.get_by_student_id(user_data.student_id):
            raise ValidationError("Student ID already registered")

        # Hash password
        hashed_password = self.get_password_hash(user_data.password)

        # Create user
        user = self.user_repo.create(user_data, hashed_password)

        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        return {"user": user, "access_token": access_token, "token_type": "bearer"}, access_token

    def login(self, email: str, password: str) -> Token:
        """Authenticate user and return access token."""
        user = self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Incorrect email or password")

        if not self.verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect email or password")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")


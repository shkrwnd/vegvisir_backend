from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
import bcrypt
import secrets
from sqlalchemy.orm import Session
from app.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.exceptions import UnauthorizedError, ValidationError, NotFoundError


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        # Bcrypt has a 72-byte limit, so truncate if necessary
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Use bcrypt directly to verify (both must be bytes)
        try:
            return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
        except Exception:
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password."""
        # Bcrypt has a 72-byte limit
        # Convert to bytes and truncate if necessary before hashing
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes
            password_bytes = password_bytes[:72]
            # Decode back to string, handling potential incomplete UTF-8 sequences
            try:
                password = password_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # If truncation broke a UTF-8 sequence, decode with error handling
                password = password_bytes.decode('utf-8', errors='ignore')
        
        # Generate salt and hash using bcrypt directly
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
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
            data={"sub": str(user.id)}, expires_delta=access_token_expires
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
            data={"sub": str(user.id)}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")

    def forgot_password(self, email: str) -> dict:
        """Generate a password reset token for a user."""
        user = self.user_repo.get_by_email(email)
        if not user:
            # Don't reveal if email exists for security
            return {"message": "If the email exists, a password reset link has been sent."}
        
        # Generate a secure random token
        reset_token = secrets.token_urlsafe(32)
        reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)  # Token expires in 1 hour
        
        # Update user with reset token
        self.user_repo.update(user, reset_token=reset_token, reset_token_expires=reset_token_expires)
        
        # In production, you would send an email with the reset token
        # For now, we'll return it in the response (remove this in production!)
        return {
            "message": "Password reset token generated. In production, this would be sent via email.",
            "reset_token": reset_token,  # Remove this in production!
            "expires_at": reset_token_expires.isoformat()
        }

    def reset_password(self, token: str, new_password: str) -> dict:
        """Reset user password using a reset token."""
        user = self.user_repo.get_by_reset_token(token)
        if not user:
            raise ValidationError("Invalid or expired reset token")
        
        # Check if token has expired
        if user.reset_token_expires and user.reset_token_expires < datetime.now(timezone.utc):
            # Clear the expired token
            self.user_repo.update(user, reset_token=None, reset_token_expires=None)
            raise ValidationError("Reset token has expired. Please request a new one.")
        
        # Hash the new password
        hashed_password = self.get_password_hash(new_password)
        
        # Update password and clear reset token
        self.user_repo.update(
            user,
            hashed_password=hashed_password,
            reset_token=None,
            reset_token_expires=None
        )
        
        return {"message": "Password has been reset successfully"}


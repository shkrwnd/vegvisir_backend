from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token, ForgotPasswordRequest, ResetPasswordRequest
from app.services.auth_service import AuthService
from app.exceptions import ValidationError, UnauthorizedError

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    - **email**: User's email address (must be unique)
    - **password**: User's password (minimum 8 characters)
    - **full_name**: User's full name
    - **student_id**: Optional student ID
    - **major**: Optional major field
    - **class_year**: Optional class year
    """
    try:
        auth_service = AuthService(db)
        result, token = auth_service.register(user_data)
        return {
            "user": UserResponse.model_validate(result["user"]).model_dump(),
            "access_token": token,
            "token_type": "bearer"
        }
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        # Log the error for debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and get access token.
    
    - **username**: User's email address (OAuth2 uses 'username' field)
    - **password**: User's password
    
    Returns a JWT access token for authenticated requests.
    """
    try:
        auth_service = AuthService(db)
        return auth_service.login(form_data.username, form_data.password)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current authenticated user information.
    
    Requires authentication via JWT token.
    """
    return UserResponse.model_validate(current_user)


@router.post("/forgot-password", response_model=dict)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Request a password reset.
    
    - **email**: User's email address
    
    Generates a password reset token. In production, this would be sent via email.
    For development, the token is returned in the response.
    """
    try:
        auth_service = AuthService(db)
        return auth_service.forgot_password(request.email)
    except Exception as e:
        # Always return success message for security (don't reveal if email exists)
        return {"message": "If the email exists, a password reset link has been sent."}


@router.post("/reset-password", response_model=dict)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset password using a reset token.
    
    - **token**: Password reset token received from forgot-password endpoint
    - **new_password**: New password (8-72 characters)
    
    The reset token expires after 1 hour.
    """
    try:
        auth_service = AuthService(db)
        return auth_service.reset_password(request.token, request.new_password)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset failed: {str(e)}"
        )


from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.models.payment import PaymentStatus, PaymentType
from app.schemas.payment import PaymentCreate
from app.services.payment_service import PaymentService
from app.exceptions import NotFoundError

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=list[dict])
def get_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[PaymentStatus] = None,
    payment_type: Optional[PaymentType] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all payments for the current user.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter by payment status
    - **payment_type**: Filter by payment type
    """
    service = PaymentService(db)
    return service.get_payments(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status,
        payment_type=payment_type,
    )


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new payment (simulation).
    
    - **payment_type**: Type of payment (event, club, dining, printing, service, other)
    - **amount**: Payment amount (must be positive)
    - **description**: Payment description
    
    Payments are created with PENDING status by default.
    Once created, payments cannot be updated or deleted.
    Complete the payment to finalize it and create a transaction record.
    """
    service = PaymentService(db)
    return service.create_payment(current_user.id, payment_data)


@router.get("/{payment_id}", response_model=dict)
def get_payment(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific payment by ID.
    """
    service = PaymentService(db)
    try:
        return service.get_payment(payment_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.post("/{payment_id}/complete", response_model=dict)
def complete_payment(
    payment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Mark a payment as completed.
    
    This simulates completing a payment transaction and automatically creates a transaction record.
    Once a payment is completed, it cannot be modified or deleted.
    """
    service = PaymentService(db)
    try:
        return service.complete_payment(payment_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


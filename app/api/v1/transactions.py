from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.models.transaction import TransactionCategory
from app.services.transaction_service import TransactionService
from app.exceptions import NotFoundError

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=list[dict])
def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[TransactionCategory] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all transactions for the current user.
    
    Note: Transactions are automatically created when payments are completed.
    They cannot be manually created, updated, or deleted.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **category**: Filter by transaction category
    - **start_date**: Filter transactions from this date
    - **end_date**: Filter transactions until this date
    """
    service = TransactionService(db)
    return service.get_transactions(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        category=category,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/analytics", response_model=dict)
def get_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get spending analytics for the current user.
    
    - **start_date**: Start date for analytics (defaults to 30 days ago)
    - **end_date**: End date for analytics (defaults to today)
    
    Returns:
    - Total spending
    - Spending by category
    - Spending over time
    """
    service = TransactionService(db)
    return service.get_analytics(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/{transaction_id}", response_model=dict)
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific transaction by ID.
    
    Note: Transactions are read-only records created automatically from completed payments.
    """
    service = TransactionService(db)
    try:
        return service.get_transaction(transaction_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


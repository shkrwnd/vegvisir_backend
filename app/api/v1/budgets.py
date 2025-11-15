from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetTracking
from app.services.budget_service import BudgetService
from app.exceptions import NotFoundError

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("/", response_model=list[dict])
def get_budgets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all budgets for the current user.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    service = BudgetService(db)
    return service.get_budgets(current_user.id, skip, limit)


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new budget.
    
    - **category**: Budget category
    - **limit_amount**: Budget limit amount (must be positive)
    - **period**: Budget period (weekly or monthly)
    - **start_date**: Budget start date
    - **end_date**: Budget end date
    """
    service = BudgetService(db)
    return service.create_budget(current_user.id, budget_data)


@router.get("/tracking", response_model=list[BudgetTracking])
def get_budgets_tracking(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all active budgets with tracking information.
    
    Returns budgets with:
    - Current spending
    - Remaining amount
    - Percentage used
    - Status (under/over/at_limit)
    """
    service = BudgetService(db)
    return service.get_all_budgets_tracking(current_user.id)


@router.get("/{budget_id}", response_model=dict)
def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific budget by ID.
    """
    service = BudgetService(db)
    try:
        return service.get_budget(budget_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.get("/{budget_id}/tracking", response_model=BudgetTracking)
def get_budget_tracking(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get budget with tracking information.
    
    Returns budget with:
    - Current spending
    - Remaining amount
    - Percentage used
    - Status (under/over/at_limit)
    """
    service = BudgetService(db)
    try:
        return service.get_budget_with_tracking(budget_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.put("/{budget_id}", response_model=dict)
def update_budget(
    budget_id: int,
    budget_data: BudgetUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a budget.
    
    Only provided fields will be updated.
    """
    service = BudgetService(db)
    try:
        return service.update_budget(budget_id, current_user.id, budget_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a budget.
    """
    service = BudgetService(db)
    try:
        service.delete_budget(budget_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


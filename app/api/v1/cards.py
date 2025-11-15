from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.card import CardCreate, CardUpdate, CardResponse
from app.services.card_service import CardService
from app.exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/cards", tags=["Cards"])


@router.get("/", response_model=list[dict])
def get_cards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all cards for the current user.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    service = CardService(db)
    return service.get_cards(current_user.id, skip, limit)


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_card(
    card_data: CardCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new card.
    
    - **card_number**: Last 4 digits of the card (must be exactly 4 digits)
    - **cardholder_name**: Name on the card
    - **expiry_date**: Card expiry date (YYYY-MM-DD format)
    - **card_type**: Type of card (debit or credit)
    - **bank_name**: Optional bank name
    - **is_default**: Whether this card should be set as default
    """
    try:
        service = CardService(db)
        return service.create_card(current_user.id, card_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.get("/{card_id}", response_model=dict)
def get_card(
    card_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific card by ID.
    """
    service = CardService(db)
    try:
        return service.get_card(card_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


@router.put("/{card_id}", response_model=dict)
def update_card(
    card_id: int,
    card_data: CardUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a card.
    
    Only provided fields will be updated.
    - **cardholder_name**: Name on the card
    - **expiry_date**: Card expiry date (YYYY-MM-DD format)
    - **bank_name**: Bank name
    - **is_default**: Whether this card should be set as default
    """
    service = CardService(db)
    try:
        return service.update_card(card_id, current_user.id, card_data)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a card.
    """
    service = CardService(db)
    try:
        service.delete_card(card_id, current_user.id)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )


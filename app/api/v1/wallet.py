from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.wallet import WalletResponse, WalletLoadRequest
from app.services.wallet_service import WalletService
from app.exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.get("/", response_model=WalletResponse)
def get_wallet(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current wallet balance (Flex Dollars).
    
    Returns the wallet information including current balance.
    If wallet doesn't exist, it will be created automatically.
    """
    service = WalletService(db)
    wallet_dict = service.get_wallet_balance(current_user.id)
    return WalletResponse(**wallet_dict)


@router.post("/load", response_model=WalletResponse, status_code=status.HTTP_200_OK)
def load_money(
    load_request: WalletLoadRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Load money into wallet from a saved card.
    
    - **amount**: Amount to load (must be greater than 0, max $10,000)
    - **card_id**: ID of the card to load money from
    
    The card must belong to the authenticated user.
    """
    try:
        service = WalletService(db)
        wallet_dict = service.load_money(current_user.id, load_request)
        return WalletResponse(**wallet_dict)
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


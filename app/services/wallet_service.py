from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.repositories.wallet_repository import WalletRepository
from app.repositories.card_repository import CardRepository
from app.repositories.transaction_repository import TransactionRepository
from app.models.transaction import TransactionCategory, PaymentMethod
from app.schemas.wallet import WalletLoadRequest
from app.schemas.transaction import TransactionCreate
from app.exceptions import NotFoundError, ValidationError


class WalletService:
    def __init__(self, db: Session):
        self.db = db
        self.wallet_repo = WalletRepository(db)
        self.card_repo = CardRepository(db)
        self.transaction_repo = TransactionRepository(db)

    def get_wallet_balance(self, user_id: int) -> dict:
        """Get current wallet balance for user. Creates wallet if it doesn't exist (lazy creation)."""
        wallet = self.wallet_repo.get_by_user_id(user_id)
        
        # Lazy creation: create wallet if it doesn't exist
        if not wallet:
            wallet = self.wallet_repo.create(user_id)
        
        return self._wallet_to_dict(wallet)

    def load_money(self, user_id: int, load_request: WalletLoadRequest) -> dict:
        """
        Load money into wallet from a card.
        
        - Validates card exists and belongs to user
        - Validates amount > 0
        - Updates wallet balance atomically
        - Creates a transaction record
        """
        # Validate card exists and belongs to user
        card = self.card_repo.get_by_id(load_request.card_id, user_id)
        if not card:
            raise NotFoundError("Card", str(load_request.card_id))
        
        # Validate amount (already validated in schema, but double-check)
        if load_request.amount <= 0:
            raise ValidationError("Amount must be greater than 0")
        
        # Get or create wallet
        wallet = self.wallet_repo.get_by_user_id(user_id)
        if not wallet:
            wallet = self.wallet_repo.create(user_id)
        
        # Update balance atomically
        updated_wallet = self.wallet_repo.update_balance(wallet, load_request.amount)
        
        # Create transaction record for wallet load
        transaction_data = TransactionCreate(
            amount=load_request.amount,
            category=TransactionCategory.SERVICES,
            merchant="Flex Dollars Wallet",
            location=None,
            payment_method=PaymentMethod.CARD,
            date=datetime.now(timezone.utc),
            description=f"Loaded ${load_request.amount:.2f} from {card.card_type.value} card ending in {card.card_number}"
        )
        
        # Create the transaction
        self.transaction_repo.create(user_id, transaction_data)
        
        return self._wallet_to_dict(updated_wallet)

    @staticmethod
    def _wallet_to_dict(wallet) -> dict:
        """Convert wallet model to dictionary."""
        return {
            "id": wallet.id,
            "user_id": wallet.user_id,
            "balance": round(wallet.balance, 2),
            "created_at": wallet.created_at.isoformat(),
            "updated_at": wallet.updated_at.isoformat(),
        }


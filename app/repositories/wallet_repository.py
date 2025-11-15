from sqlalchemy.orm import Session
from typing import Optional
from app.models.wallet import Wallet


class WalletRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int) -> Optional[Wallet]:
        """Get wallet by user ID."""
        return self.db.query(Wallet).filter(
            Wallet.user_id == user_id
        ).first()

    def create(self, user_id: int) -> Wallet:
        """Create a new wallet for a user."""
        db_wallet = Wallet(
            user_id=user_id,
            balance=0.0
        )
        self.db.add(db_wallet)
        self.db.commit()
        self.db.refresh(db_wallet)
        return db_wallet

    def update_balance(self, wallet: Wallet, amount: float) -> Wallet:
        """Add amount to wallet balance (atomic operation)."""
        wallet.balance += amount
        # Round to 2 decimal places to avoid floating point precision issues
        wallet.balance = round(wallet.balance, 2)
        self.db.commit()
        self.db.refresh(wallet)
        return wallet


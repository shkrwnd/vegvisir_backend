from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.repositories.transaction_repository import TransactionRepository
from app.models.transaction import TransactionCategory
from app.schemas.transaction import TransactionCreate, TransactionUpdate
from app.exceptions import NotFoundError


class TransactionService:
    def __init__(self, db: Session):
        self.db = db
        self.transaction_repo = TransactionRepository(db)

    def get_transactions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        category: Optional[TransactionCategory] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[dict]:
        """Get all transactions for a user."""
        transactions = self.transaction_repo.get_all(
            user_id=user_id,
            skip=skip,
            limit=limit,
            category=category,
            start_date=start_date,
            end_date=end_date,
        )
        return [self._transaction_to_dict(t) for t in transactions]

    def get_transaction(self, transaction_id: int, user_id: int) -> dict:
        """Get a single transaction by ID."""
        transaction = self.transaction_repo.get_by_id(transaction_id, user_id)
        if not transaction:
            raise NotFoundError("Transaction", str(transaction_id))
        return self._transaction_to_dict(transaction)

    def create_transaction(self, user_id: int, transaction_data: TransactionCreate) -> dict:
        """Create a new transaction."""
        transaction = self.transaction_repo.create(user_id, transaction_data)
        return self._transaction_to_dict(transaction)

    def update_transaction(
        self, transaction_id: int, user_id: int, transaction_data: TransactionUpdate
    ) -> dict:
        """Update a transaction."""
        transaction = self.transaction_repo.get_by_id(transaction_id, user_id)
        if not transaction:
            raise NotFoundError("Transaction", str(transaction_id))
        
        updated_transaction = self.transaction_repo.update(transaction, transaction_data)
        return self._transaction_to_dict(updated_transaction)

    def delete_transaction(self, transaction_id: int, user_id: int) -> None:
        """Delete a transaction."""
        transaction = self.transaction_repo.get_by_id(transaction_id, user_id)
        if not transaction:
            raise NotFoundError("Transaction", str(transaction_id))
        self.transaction_repo.delete(transaction)

    def get_analytics(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        """Get spending analytics for a user."""
        # Get total spending by category
        spending_by_category = self.transaction_repo.get_total_by_category(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
        )

        # Get spending over time (last 30 days if no dates provided)
        if not start_date or not end_date:
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)

        spending_over_time = self.transaction_repo.get_spending_over_time(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            group_by="day"
        )

        # Calculate total spending
        total_spending = sum(item["total"] for item in spending_by_category)

        return {
            "total_spending": total_spending,
            "spending_by_category": spending_by_category,
            "spending_over_time": spending_over_time,
            "period": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
            }
        }

    @staticmethod
    def _transaction_to_dict(transaction) -> dict:
        """Convert transaction model to dictionary."""
        return {
            "id": transaction.id,
            "user_id": transaction.user_id,
            "amount": transaction.amount,
            "category": transaction.category.value,
            "merchant": transaction.merchant,
            "location": transaction.location,
            "payment_method": transaction.payment_method.value,
            "date": transaction.date.isoformat(),
            "description": transaction.description,
            "created_at": transaction.created_at.isoformat(),
        }


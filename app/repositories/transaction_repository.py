from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime, date
from app.models.transaction import Transaction, TransactionCategory
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, transaction_id: int, user_id: int) -> Optional[Transaction]:
        """Get transaction by ID for a specific user."""
        return self.db.query(Transaction).filter(
            and_(Transaction.id == transaction_id, Transaction.user_id == user_id)
        ).first()

    def get_all(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        category: Optional[TransactionCategory] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Transaction]:
        """Get all transactions for a user with optional filters."""
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)

        if category:
            query = query.filter(Transaction.category == category)
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        return query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()

    def create(self, user_id: int, transaction_data: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        db_transaction = Transaction(
            user_id=user_id,
            **transaction_data.model_dump()
        )
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def update(self, transaction: Transaction, transaction_data: TransactionUpdate) -> Transaction:
        """Update a transaction."""
        update_data = transaction_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(transaction, key, value)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction) -> None:
        """Delete a transaction."""
        self.db.delete(transaction)
        self.db.commit()

    def get_total_by_category(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[dict]:
        """Get total spending by category."""
        query = self.db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("total")
        ).filter(Transaction.user_id == user_id)

        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)

        results = query.group_by(Transaction.category).all()
        return [
            {"category": category.value, "total": float(total)}
            for category, total in results
        ]

    def get_spending_over_time(
        self,
        user_id: int,
        start_date: datetime,
        end_date: datetime,
        group_by: str = "day"
    ) -> List[dict]:
        """Get spending over time grouped by day, week, or month."""
        query = self.db.query(
            func.date_trunc(group_by, Transaction.date).label("period"),
            func.sum(Transaction.amount).label("total")
        ).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )
        ).group_by("period").order_by("period")

        results = query.all()
        return [
            {"period": str(period), "total": float(total)}
            for period, total in results
        ]


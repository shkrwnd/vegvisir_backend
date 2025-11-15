from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from datetime import date
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, budget_id: int, user_id: int) -> Optional[Budget]:
        """Get budget by ID for a specific user."""
        return self.db.query(Budget).filter(
            and_(Budget.id == budget_id, Budget.user_id == user_id)
        ).first()

    def get_all(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Budget]:
        """Get all budgets for a user."""
        return (
            self.db.query(Budget)
            .filter(Budget.user_id == user_id)
            .order_by(Budget.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active_budgets(self, user_id: int, current_date: date = None) -> List[Budget]:
        """Get all active budgets (where current date is between start and end date)."""
        if current_date is None:
            current_date = date.today()
        
        return (
            self.db.query(Budget)
            .filter(
                and_(
                    Budget.user_id == user_id,
                    Budget.start_date <= current_date,
                    Budget.end_date >= current_date
                )
            )
            .all()
        )

    def create(self, user_id: int, budget_data: BudgetCreate) -> Budget:
        """Create a new budget."""
        db_budget = Budget(
            user_id=user_id,
            **budget_data.model_dump()
        )
        self.db.add(db_budget)
        self.db.commit()
        self.db.refresh(db_budget)
        return db_budget

    def update(self, budget: Budget, budget_data: BudgetUpdate) -> Budget:
        """Update a budget."""
        update_data = budget_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(budget, key, value)
        self.db.commit()
        self.db.refresh(budget)
        return budget

    def delete(self, budget: Budget) -> None:
        """Delete a budget."""
        self.db.delete(budget)
        self.db.commit()


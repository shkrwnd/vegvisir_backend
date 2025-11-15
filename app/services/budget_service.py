from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.repositories.budget_repository import BudgetRepository
from app.repositories.transaction_repository import TransactionRepository
from app.models.transaction import TransactionCategory
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetTracking
from app.exceptions import NotFoundError


class BudgetService:
    def __init__(self, db: Session):
        self.db = db
        self.budget_repo = BudgetRepository(db)
        self.transaction_repo = TransactionRepository(db)

    def get_budgets(self, user_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all budgets for a user."""
        budgets = self.budget_repo.get_all(user_id, skip, limit)
        return [self._budget_to_dict(b) for b in budgets]

    def get_budget(self, budget_id: int, user_id: int) -> dict:
        """Get a single budget by ID."""
        budget = self.budget_repo.get_by_id(budget_id, user_id)
        if not budget:
            raise NotFoundError("Budget", str(budget_id))
        return self._budget_to_dict(budget)

    def get_budget_with_tracking(self, budget_id: int, user_id: int) -> BudgetTracking:
        """Get budget with tracking information."""
        budget = self.budget_repo.get_by_id(budget_id, user_id)
        if not budget:
            raise NotFoundError("Budget", str(budget_id))
        
        tracking = self._calculate_budget_tracking(budget, user_id)
        return tracking

    def create_budget(self, user_id: int, budget_data: BudgetCreate) -> dict:
        """Create a new budget."""
        budget = self.budget_repo.create(user_id, budget_data)
        return self._budget_to_dict(budget)

    def update_budget(
        self, budget_id: int, user_id: int, budget_data: BudgetUpdate
    ) -> dict:
        """Update a budget."""
        budget = self.budget_repo.get_by_id(budget_id, user_id)
        if not budget:
            raise NotFoundError("Budget", str(budget_id))
        
        updated_budget = self.budget_repo.update(budget, budget_data)
        return self._budget_to_dict(updated_budget)

    def delete_budget(self, budget_id: int, user_id: int) -> None:
        """Delete a budget."""
        budget = self.budget_repo.get_by_id(budget_id, user_id)
        if not budget:
            raise NotFoundError("Budget", str(budget_id))
        self.budget_repo.delete(budget)

    def get_all_budgets_tracking(self, user_id: int) -> List[BudgetTracking]:
        """Get all budgets with tracking information."""
        budgets = self.budget_repo.get_active_budgets(user_id)
        return [self._calculate_budget_tracking(budget, user_id) for budget in budgets]

    def _calculate_budget_tracking(self, budget, user_id: int) -> BudgetTracking:
        """Calculate budget tracking information."""
        # Try to match budget category to TransactionCategory enum
        category_filter = None
        try:
            # Try to find matching TransactionCategory enum value
            for cat in TransactionCategory:
                if cat.value.lower() == budget.category.lower():
                    category_filter = cat
                    break
        except (ValueError, AttributeError):
            pass
        
        # Get transactions for this budget's category and date range
        transactions = self.transaction_repo.get_all(
            user_id=user_id,
            category=category_filter,
            start_date=datetime.combine(budget.start_date, datetime.min.time()),
            end_date=datetime.combine(budget.end_date, datetime.max.time()),
        )
        
        # Calculate current spending
        current_spending = sum(t.amount for t in transactions)
        
        # Calculate remaining amount
        remaining_amount = budget.limit_amount - current_spending
        
        # Calculate percentage used
        percentage_used = (current_spending / budget.limit_amount * 100) if budget.limit_amount > 0 else 0
        
        # Determine status
        if current_spending > budget.limit_amount:
            status = "over"
        elif current_spending == budget.limit_amount:
            status = "at_limit"
        else:
            status = "under"
        
        return BudgetTracking(
            id=budget.id,
            user_id=budget.user_id,
            category=budget.category,
            limit_amount=budget.limit_amount,
            period=budget.period,
            start_date=budget.start_date,
            end_date=budget.end_date,
            created_at=budget.created_at,
            updated_at=budget.updated_at,
            current_spending=current_spending,
            remaining_amount=remaining_amount,
            percentage_used=round(percentage_used, 2),
            status=status
        )

    @staticmethod
    def _budget_to_dict(budget) -> dict:
        """Convert budget model to dictionary."""
        return {
            "id": budget.id,
            "user_id": budget.user_id,
            "category": budget.category,
            "limit_amount": budget.limit_amount,
            "period": budget.period.value,
            "start_date": budget.start_date.isoformat(),
            "end_date": budget.end_date.isoformat(),
            "created_at": budget.created_at.isoformat(),
            "updated_at": budget.updated_at.isoformat(),
        }


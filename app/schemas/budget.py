from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from app.models.budget import BudgetPeriod


class BudgetBase(BaseModel):
    category: str = Field(..., min_length=1, max_length=100)
    limit_amount: float = Field(..., gt=0)
    period: BudgetPeriod
    start_date: date
    end_date: date


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    limit_amount: Optional[float] = Field(None, gt=0)
    period: Optional[BudgetPeriod] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Budget(BudgetResponse):
    pass


class BudgetTracking(BudgetResponse):
    current_spending: float
    remaining_amount: float
    percentage_used: float
    status: str  # "under", "over", "at_limit"


from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.transaction import TransactionCategory, PaymentMethod


class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    category: TransactionCategory
    merchant: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    payment_method: PaymentMethod
    date: datetime
    description: Optional[str] = Field(None, max_length=500)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[TransactionCategory] = None
    merchant: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    payment_method: Optional[PaymentMethod] = None
    date: Optional[datetime] = None
    description: Optional[str] = Field(None, max_length=500)


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Transaction(TransactionResponse):
    pass


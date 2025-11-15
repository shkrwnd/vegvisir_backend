from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional
from app.models.card import CardType


class CardBase(BaseModel):
    card_number: str = Field(..., min_length=4, max_length=4, description="Last 4 digits of the card")
    cardholder_name: str = Field(..., min_length=1, max_length=255)
    expiry_date: date
    card_type: CardType
    bank_name: Optional[str] = Field(None, max_length=100)
    is_default: bool = Field(default=False)

    @field_validator('card_number')
    @classmethod
    def validate_card_number(cls, v: str) -> str:
        """Validate that card_number contains only digits."""
        if not v.isdigit():
            raise ValueError('Card number must contain only digits')
        if len(v) != 4:
            raise ValueError('Card number must be exactly 4 digits')
        return v


class CardCreate(CardBase):
    pass


class CardUpdate(BaseModel):
    cardholder_name: Optional[str] = Field(None, min_length=1, max_length=255)
    expiry_date: Optional[date] = None
    bank_name: Optional[str] = Field(None, max_length=100)
    is_default: Optional[bool] = None


class CardResponse(CardBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Card(CardResponse):
    pass


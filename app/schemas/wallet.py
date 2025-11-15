from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class WalletResponse(BaseModel):
    """Response schema for wallet information."""
    id: int
    user_id: int
    balance: float = Field(..., description="Current Flex Dollars balance")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class WalletLoadRequest(BaseModel):
    """Request schema for loading money into wallet."""
    amount: float = Field(..., gt=0, le=10000, description="Amount to load (must be greater than 0 and not exceed $10,000)")
    card_id: int = Field(..., description="ID of the card to load money from")

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Validate that amount has reasonable precision and round to 2 decimal places."""
        # Round to 2 decimal places
        return round(v, 2)


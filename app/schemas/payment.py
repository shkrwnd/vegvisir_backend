from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from app.models.payment import PaymentType, PaymentStatus


class PaymentBase(BaseModel):
    payment_type: PaymentType
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)
    vendor_id: Optional[int] = Field(None, description="ID of the vendor (for Raider card payments)")

    @field_validator('payment_type', mode='before')
    @classmethod
    def normalize_payment_type(cls, v):
        """Normalize payment_type to uppercase to match enum values."""
        if isinstance(v, str):
            v_upper = v.upper()
            # Try to match it to a PaymentType enum value
            for payment_type in PaymentType:
                if payment_type.value == v_upper:
                    return payment_type
            # If no match, return the uppercase string and let Pydantic validation handle the error
            return v_upper
        return v


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    payment_type: Optional[PaymentType] = None
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    status: Optional[PaymentStatus] = None


class PaymentResponse(PaymentBase):
    id: int
    user_id: int
    vendor_id: Optional[int]
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Payment(PaymentResponse):
    pass


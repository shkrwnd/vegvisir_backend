from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.payment import PaymentType, PaymentStatus


class PaymentBase(BaseModel):
    payment_type: PaymentType
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=500)
    vendor_id: Optional[int] = Field(None, description="ID of the vendor (for Raider card payments)")


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


from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class VendorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    location: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=500)
    hours: Optional[str] = Field(None, max_length=500)
    accepts_raider_card: bool = True
    accepts_meal_plan: bool = True
    is_active: bool = True


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    location: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, max_length=500)
    hours: Optional[str] = Field(None, max_length=500)
    accepts_raider_card: Optional[bool] = None
    accepts_meal_plan: Optional[bool] = None
    is_active: Optional[bool] = None


class VendorResponse(VendorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Vendor(VendorResponse):
    pass

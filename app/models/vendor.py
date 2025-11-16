from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    category = Column(String, nullable=False)  # e.g., "dining", "retail", "service", "entertainment"
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)  # Campus location
    latitude = Column(Float, nullable=True)  # Geographic latitude for map display
    longitude = Column(Float, nullable=True)  # Geographic longitude for map display
    logo_url = Column(String, nullable=True)  # URL to vendor logo
    hours = Column(String, nullable=True)  # Operating hours
    # `accepts_raider_card` indicates the vendor accepts payments via the Raider card (real money).
    accepts_raider_card = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    payments = relationship("Payment", back_populates="vendor")

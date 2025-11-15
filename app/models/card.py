from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class CardType(str, enum.Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    card_number = Column(String, nullable=False)  # Last 4 digits only (masked)
    cardholder_name = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=False)
    card_type = Column(Enum(CardType), nullable=False)
    bank_name = Column(String, nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="cards")


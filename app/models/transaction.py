from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class TransactionCategory(str, enum.Enum):
    DINING = "dining"
    BOOKS = "books"
    TRANSPORTATION = "transportation"
    ENTERTAINMENT = "entertainment"
    SERVICES = "services"
    OTHER = "other"


class PaymentMethod(str, enum.Enum):
    CARD = "card"
    CASH = "cash"
    MOBILE = "mobile"
    CAMPUS_CARD = "campus_card"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    merchant = Column(String, nullable=False)
    location = Column(String, nullable=True)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="transactions")


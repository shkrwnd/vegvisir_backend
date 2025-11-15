from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class BudgetPeriod(str, enum.Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    limit_amount = Column(Float, nullable=False)
    period = Column(Enum(BudgetPeriod), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="budgets")


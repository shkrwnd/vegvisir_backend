from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from app.models.payment import Payment, PaymentStatus, PaymentType
from app.schemas.payment import PaymentCreate, PaymentUpdate


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, payment_id: int, user_id: int) -> Optional[Payment]:
        """Get payment by ID for a specific user."""
        return self.db.query(Payment).filter(
            and_(Payment.id == payment_id, Payment.user_id == user_id)
        ).first()

    def get_all(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[PaymentStatus] = None,
        payment_type: Optional[PaymentType] = None,
    ) -> List[Payment]:
        """Get all payments for a user with optional filters."""
        query = self.db.query(Payment).filter(Payment.user_id == user_id)

        if status:
            query = query.filter(Payment.status == status)
        if payment_type:
            query = query.filter(Payment.payment_type == payment_type)

        return query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()

    def create(self, user_id: int, payment_data: PaymentCreate) -> Payment:
        """Create a new payment."""
        db_payment = Payment(
            user_id=user_id,
            **payment_data.model_dump()
        )
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment

    def update(self, payment: Payment, payment_data: PaymentUpdate) -> Payment:
        """Update a payment."""
        update_data = payment_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(payment, key, value)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update_status(self, payment: Payment, status: PaymentStatus) -> Payment:
        """Update payment status."""
        payment.status = status
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def delete(self, payment: Payment) -> None:
        """Delete a payment."""
        self.db.delete(payment)
        self.db.commit()


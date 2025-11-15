from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.repositories.payment_repository import PaymentRepository
from app.repositories.transaction_repository import TransactionRepository
from app.models.payment import PaymentStatus, PaymentType
from app.models.transaction import TransactionCategory, PaymentMethod
from app.schemas.payment import PaymentCreate
from app.schemas.transaction import TransactionCreate
from app.exceptions import NotFoundError


class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)
        self.transaction_repo = TransactionRepository(db)

    def get_payments(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[PaymentStatus] = None,
        payment_type: Optional[PaymentType] = None,
    ) -> List[dict]:
        """Get all payments for a user."""
        payments = self.payment_repo.get_all(
            user_id=user_id,
            skip=skip,
            limit=limit,
            status=status,
            payment_type=payment_type,
        )
        return [self._payment_to_dict(p) for p in payments]

    def get_payment(self, payment_id: int, user_id: int) -> dict:
        """Get a single payment by ID."""
        payment = self.payment_repo.get_by_id(payment_id, user_id)
        if not payment:
            raise NotFoundError("Payment", str(payment_id))
        return self._payment_to_dict(payment)

    def create_payment(self, user_id: int, payment_data: PaymentCreate) -> dict:
        """Create a new payment (simulation)."""
        payment = self.payment_repo.create(user_id, payment_data)
        return self._payment_to_dict(payment)

    def complete_payment(self, payment_id: int, user_id: int) -> dict:
        """Mark a payment as completed and create a transaction."""
        payment = self.payment_repo.get_by_id(payment_id, user_id)
        if not payment:
            raise NotFoundError("Payment", str(payment_id))
        
        # Only create transaction if payment is being completed (not already completed)
        if payment.status != PaymentStatus.COMPLETED:
            # Map payment type to transaction category
            category_map = {
                PaymentType.DINING: TransactionCategory.DINING,
                PaymentType.EVENT: TransactionCategory.ENTERTAINMENT,
                PaymentType.CLUB: TransactionCategory.ENTERTAINMENT,
                PaymentType.PRINTING: TransactionCategory.SERVICES,
                PaymentType.SERVICE: TransactionCategory.SERVICES,
                PaymentType.OTHER: TransactionCategory.OTHER,
            }
            
            # Create transaction from completed payment
            transaction_data = TransactionCreate(
                amount=payment.amount,
                category=category_map.get(payment.payment_type, TransactionCategory.OTHER),
                merchant=payment.description[:255] if len(payment.description) <= 255 else payment.description[:252] + "...",
                location=None,
                payment_method=PaymentMethod.CAMPUS_CARD,  # Default for campus payments
                date=datetime.utcnow(),
                description=f"Payment: {payment.description}"
            )
            
            # Create the transaction
            self.transaction_repo.create(user_id, transaction_data)
        
        # Update payment status to completed
        completed_payment = self.payment_repo.update_status(payment, PaymentStatus.COMPLETED)
        return self._payment_to_dict(completed_payment)

    @staticmethod
    def _payment_to_dict(payment) -> dict:
        """Convert payment model to dictionary."""
        return {
            "id": payment.id,
            "user_id": payment.user_id,
            "payment_type": payment.payment_type.value,
            "amount": payment.amount,
            "description": payment.description,
            "status": payment.status.value,
            "created_at": payment.created_at.isoformat(),
            "updated_at": payment.updated_at.isoformat(),
        }


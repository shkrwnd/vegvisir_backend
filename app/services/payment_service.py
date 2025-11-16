from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.repositories.payment_repository import PaymentRepository
from app.repositories.transaction_repository import TransactionRepository
from app.models.payment import PaymentStatus, PaymentType
from app.models.transaction import TransactionCategory, PaymentMethod
from app.models.wallet import Wallet
from app.schemas.payment import PaymentCreate
from app.schemas.transaction import TransactionCreate
from app.exceptions import NotFoundError, ValidationError


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
        """Create a new payment (simulation).
        
        Business Rules:
        - Amount must be positive
        - Amount cannot exceed wallet balance
        - Wallet must exist
        - Creates a payment record
        - Immediately creates a transaction and logs it
        - Deducts the amount from user's wallet balance
        
        Automatically maps vendor category to valid PaymentType if needed.
        """
        # 1. Validate amount is positive
        if payment_data.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero")
        
        # 2. Check wallet exists and has sufficient balance
        wallet = self.db.query(Wallet).filter(Wallet.user_id == user_id).with_for_update().first()
        if not wallet:
            raise ValidationError("User wallet not found. Please initialize wallet first.")

        if payment_data.amount > wallet.balance:
            raise ValidationError(
                f"Insufficient balance. Required: ${payment_data.amount:.2f}, "
                f"Available: ${wallet.balance:.2f}"
            )
        
        # 3. Normalize payment_type
        try:
            if isinstance(payment_data.payment_type, PaymentType):
                payment = self.payment_repo.create(user_id, payment_data)
            else:
                payment_type_str = str(payment_data.payment_type).upper()
                category_to_payment_type = {
                    "DINING": PaymentType.DINING,
                    "RETAIL": PaymentType.RETAIL,
                    "SERVICE": PaymentType.SERVICE,
                    "SERVICES": PaymentType.SERVICES,
                    "ENTERTAINMENT": PaymentType.ENTERTAINMENT,
                    "EVENT": PaymentType.EVENT,
                    "CLUB": PaymentType.CLUB,
                    "PRINTING": PaymentType.PRINTING,
                    "OTHER": PaymentType.OTHER,
                }
                
                if payment_type_str in category_to_payment_type:
                    payment_data.payment_type = category_to_payment_type[payment_type_str]
                else:
                    payment_data.payment_type = PaymentType[payment_type_str]
                
                payment = self.payment_repo.create(user_id, payment_data)
        except Exception as e:
            raise ValidationError(f"Invalid payment type: {payment_data.payment_type}")
        
        # 4. Immediately create a transaction for the payment
        category_map = {
            PaymentType.DINING: TransactionCategory.DINING,
            PaymentType.EVENT: TransactionCategory.ENTERTAINMENT,
            PaymentType.CLUB: TransactionCategory.ENTERTAINMENT,
            PaymentType.PRINTING: TransactionCategory.SERVICES,
            PaymentType.SERVICE: TransactionCategory.SERVICES,
            PaymentType.SERVICES: TransactionCategory.SERVICES,
            PaymentType.RETAIL: TransactionCategory.OTHER,
            PaymentType.ENTERTAINMENT: TransactionCategory.ENTERTAINMENT,
            PaymentType.OTHER: TransactionCategory.OTHER,
        }
        
        transaction_data = TransactionCreate(
            amount=payment.amount,
            category=category_map.get(payment.payment_type, TransactionCategory.OTHER),
            merchant=payment.description[:255] if len(payment.description) <= 255 else payment.description[:252] + "...",
            location=None,
            payment_method=PaymentMethod.CAMPUS_CARD,
            date=datetime.utcnow(),
            description=f"Payment: {payment.description}"
        )
        
        # 5. Create the transaction
        self.transaction_repo.create(user_id, transaction_data)

        # 6. Deduct amount from user's wallet balance
        # (wallet is already locked from step 2)
        wallet.balance -= payment.amount
        self.db.commit()

        return self._payment_to_dict(payment)

    def complete_payment(self, payment_id: int, user_id: int) -> dict:
        """Mark a payment as completed.

        Note: Transactions are created immediately when payment is created,
        so this endpoint only updates the payment status.
        """
        payment = self.payment_repo.get_by_id(payment_id, user_id)
        if not payment:
            raise NotFoundError("Payment", str(payment_id))

        # Update payment status to completed
        # Transaction was already created in create_payment()
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


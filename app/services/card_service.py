from sqlalchemy.orm import Session
from typing import List
from app.repositories.card_repository import CardRepository
from app.schemas.card import CardCreate, CardUpdate
from app.exceptions import NotFoundError


class CardService:
    def __init__(self, db: Session):
        self.db = db
        self.card_repo = CardRepository(db)

    def get_cards(self, user_id: int, skip: int = 0, limit: int = 100) -> List[dict]:
        """Get all cards for a user."""
        cards = self.card_repo.get_all(user_id, skip, limit)
        return [self._card_to_dict(c) for c in cards]

    def get_card(self, card_id: int, user_id: int) -> dict:
        """Get a single card by ID."""
        card = self.card_repo.get_by_id(card_id, user_id)
        if not card:
            raise NotFoundError("Card", str(card_id))
        return self._card_to_dict(card)

    def create_card(self, user_id: int, card_data: CardCreate) -> dict:
        """Create a new card."""
        card = self.card_repo.create(user_id, card_data)
        return self._card_to_dict(card)

    def update_card(self, card_id: int, user_id: int, card_data: CardUpdate) -> dict:
        """Update a card."""
        card = self.card_repo.get_by_id(card_id, user_id)
        if not card:
            raise NotFoundError("Card", str(card_id))
        
        updated_card = self.card_repo.update(card, card_data)
        return self._card_to_dict(updated_card)

    def delete_card(self, card_id: int, user_id: int) -> None:
        """Delete a card."""
        card = self.card_repo.get_by_id(card_id, user_id)
        if not card:
            raise NotFoundError("Card", str(card_id))
        self.card_repo.delete(card)

    @staticmethod
    def _card_to_dict(card) -> dict:
        """Convert card model to dictionary."""
        return {
            "id": card.id,
            "user_id": card.user_id,
            "card_number": card.card_number,
            "cardholder_name": card.cardholder_name,
            "expiry_date": card.expiry_date.isoformat(),
            "card_type": card.card_type.value,
            "bank_name": card.bank_name,
            "is_default": card.is_default,
            "created_at": card.created_at.isoformat(),
            "updated_at": card.updated_at.isoformat(),
        }


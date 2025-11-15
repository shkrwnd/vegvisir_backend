from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.card import Card
from app.schemas.card import CardCreate, CardUpdate


class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, card_id: int, user_id: int) -> Optional[Card]:
        """Get card by ID for a specific user."""
        return self.db.query(Card).filter(
            Card.id == card_id,
            Card.user_id == user_id
        ).first()

    def get_all(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Card]:
        """Get all cards for a user."""
        return self.db.query(Card).filter(
            Card.user_id == user_id
        ).offset(skip).limit(limit).all()

    def get_default(self, user_id: int) -> Optional[Card]:
        """Get the default card for a user."""
        return self.db.query(Card).filter(
            Card.user_id == user_id,
            Card.is_default == True
        ).first()

    def create(self, user_id: int, card_data: CardCreate) -> Card:
        """Create a new card."""
        # If this is set as default, unset other default cards
        if card_data.is_default:
            self._unset_default_cards(user_id)
        
        db_card = Card(
            user_id=user_id,
            card_number=card_data.card_number,
            cardholder_name=card_data.cardholder_name,
            expiry_date=card_data.expiry_date,
            card_type=card_data.card_type,
            bank_name=card_data.bank_name,
            is_default=card_data.is_default
        )
        self.db.add(db_card)
        self.db.commit()
        self.db.refresh(db_card)
        return db_card

    def update(self, card: Card, card_data: CardUpdate) -> Card:
        """Update a card."""
        update_data = card_data.model_dump(exclude_unset=True)
        
        # If setting as default, unset other default cards
        if update_data.get('is_default') is True:
            self._unset_default_cards(card.user_id, exclude_card_id=card.id)
        
        for field, value in update_data.items():
            setattr(card, field, value)
        
        self.db.commit()
        self.db.refresh(card)
        return card

    def delete(self, card: Card) -> None:
        """Delete a card."""
        self.db.delete(card)
        self.db.commit()

    def _unset_default_cards(self, user_id: int, exclude_card_id: Optional[int] = None) -> None:
        """Unset all default cards for a user, optionally excluding a specific card."""
        query = self.db.query(Card).filter(
            Card.user_id == user_id,
            Card.is_default == True
        )
        if exclude_card_id:
            query = query.filter(Card.id != exclude_card_id)
        
        default_cards = query.all()
        for card in default_cards:
            card.is_default = False
        self.db.commit()


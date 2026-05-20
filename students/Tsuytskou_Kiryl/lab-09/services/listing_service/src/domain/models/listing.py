from datetime import datetime
from typing import List, Optional
from src.domain.models.price import Price
from src.domain.models.category import Category
from src.domain.exceptions.domain_exception import InvalidListingStateError


class Listing:
    """Aggregate Root: Сущность объявления"""

    def __init__(self, listing_id: str, seller_id: str, title: str,
                 description: str, price: Price, category: Category,
                 images: List[str] = None):
        self.id = listing_id
        self.seller_id = seller_id
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.images = images or []
        self.status = "PENDING_MODERATION"
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.events = []
        self._validate()

    def _validate(self):
        if len(self.title) < 5:
            raise ValueError("Название должно содержать минимум 5 символов")
        if len(self.description) > 5000:
            raise ValueError("Описание не должно превышать 5000 символов")

    def _add_event(self, event_name: str, **kwargs):
        self.events.append({
            "event": event_name,
            "listing_id": self.id,
            "occurred_at": datetime.now(),
            **kwargs
        })

    def approve(self):
        if self.status != "PENDING_MODERATION":
            raise InvalidListingStateError("Можно одобрить только объявление на модерации")
        self.status = "ACTIVE"
        self.updated_at = datetime.now()
        self._add_event("ListingApproved")

    def reject(self, reason: str):
        if self.status != "PENDING_MODERATION":
            raise InvalidListingStateError("Можно отклонить только объявление на модерации")
        self.status = "REJECTED"
        self.updated_at = datetime.now()
        self._add_event("ListingRejected", reason=reason)

    def mark_as_sold(self):
        if self.status != "ACTIVE":
            raise InvalidListingStateError("Можно отметить как проданное только активное объявление")
        self.status = "SOLD"
        self.updated_at = datetime.now()
        self._add_event("ListingSold")

    def archive(self):
        if self.status not in ["ACTIVE", "SOLD"]:
            raise InvalidListingStateError("Можно архивировать только активное или проданное объявление")
        self.status = "ARCHIVED"
        self.updated_at = datetime.now()
        self._add_event("ListingArchived")

    def __eq__(self, other):
        if not isinstance(other, Listing):
            return False
        return self.id == other.id

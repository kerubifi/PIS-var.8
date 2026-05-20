from datetime import datetime
from typing import List, Optional
from .price import Price
from .category import Category
from src.domain.exceptions.domain_exception import InvalidListingStateError


class Listing:
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
        self.events = []
        self._validate()

    def _validate(self):
        if len(self.title) < 5:
            raise ValueError("Название должно содержать минимум 5 символов")
        if len(self.description) > 5000:
            raise ValueError("Описание не должно превышать 5000 символов")

    def approve(self):
        if self.status != "PENDING_MODERATION":
            raise InvalidListingStateError("Можно одобрить только объявление на модерации")
        self.status = "ACTIVE"
        self.events.append({"event": "ListingApproved", "listing_id": self.id, "occurred_at": datetime.now()})

    def reject(self, reason: str):
        if self.status != "PENDING_MODERATION":
            raise InvalidListingStateError("Можно отклонить только объявление на модерации")
        self.status = "REJECTED"
        self.events.append({"event": "ListingRejected", "listing_id": self.id, "reason": reason, "occurred_at": datetime.now()})

    def mark_as_sold(self):
        if self.status != "ACTIVE":
            raise InvalidListingStateError("Можно отметить как проданное только активное объявление")
        self.status = "SOLD"
        self.events.append({"event": "ListingSold", "listing_id": self.id, "occurred_at": datetime.now()})

    def archive(self):
        if self.status not in ["ACTIVE", "SOLD"]:
            raise InvalidListingStateError("Можно архивировать только активное или проданное объявление")
        self.status = "ARCHIVED"
        self.events.append({"event": "ListingArchived", "listing_id": self.id, "occurred_at": datetime.now()})

    def __eq__(self, other):
        if not isinstance(other, Listing):
            return False
        return self.id == other.id

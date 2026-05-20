from datetime import datetime
from typing import List
from .price import Price
from .category import Category


class Listing:
    """Domain entity: Listing"""

    def __init__(self, listing_id: str, seller_id: str, title: str, description: str, 
                 price: Price, images: List[str] = None):
        self.id = listing_id
        self.seller_id = seller_id
        self.title = title
        self.description = description
        self.price = price
        self.images = images or []
        self.status = "PENDING_MODERATION"
        self.created_at = datetime.now()
        self._validate()

    def _validate(self):
        """Validation of listing fields"""
        if len(self.title) < 5:
            raise ValueError("Название должно содержать минимум 5 символов")
        if len(self.description) > 5000:
            raise ValueError("Описание не должно превышать 5000 символов")

    def approve(self):
        """Approve listing (from PENDING_MODERATION to ACTIVE)"""
        if self.status != "PENDING_MODERATION":
            raise ValueError("Can only approve listing under moderation")
        self.status = "ACTIVE"

    def reject(self, reason: str):
        """Reject listing with reason"""
        if self.status != "PENDING_MODERATION":
            raise ValueError("Can only reject listing under moderation")
        self.status = "REJECTED"
        # In real system we could save reason to separate field

    def mark_as_sold(self):
        """Mark listing as sold"""
        if self.status != "ACTIVE":
            raise ValueError("Can only mark as sold active listing")
        self.status = "SOLD"

    def archive(self):
        """Archive listing"""
        if self.status not in ["ACTIVE", "SOLD"]:
            raise ValueError("Can only archive active or sold listing")
        self.status = "ARCHIVED"

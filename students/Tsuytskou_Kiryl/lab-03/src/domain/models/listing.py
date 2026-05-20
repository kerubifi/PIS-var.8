from datetime import datetime
from typing import Set, List
from src.domain.models.price import Price
from src.domain.models.category import Category


class Listing:
    """Aggregate Root: Сущность объявления"""

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
        self.tags: Set[Category] = set()
        self.events = []  # Регистрация доменных событий
        self._validate()

    def _validate(self):
        """Валидация полей объявления"""
        if len(self.title) < 5:
            raise ValueError("Название должно содержать минимум 5 символов")
        if len(self.description) > 5000:
            raise ValueError("Описание не должно превышать 5000 символов")

    def add_category(self, category: Category):
        if self.status in ["ACTIVE", "SOLD"]:
            raise ValueError("Нельзя менять категории у опубликованного или проданного объявления")
        self.tags.add(category)

    def approve(self):
        """Одобрить объявление (из PENDING_MODERATION в ACTIVE)"""
        if self.status != "PENDING_MODERATION":
            raise ValueError("Можно одобрить только объявление на модерации")
        self.status = "ACTIVE"
        # Регистрируем событие одобрения
        self.events.append({
            "event": "ListingApproved",
            "listing_id": self.id,
            "occurred_at": datetime.now()
        })

    def reject(self, reason: str):
        """Отклонить объявление с указанием причины"""
        if self.status != "PENDING_MODERATION":
            raise ValueError("Можно отклонить только объявление на модерации")
        self.status = "REJECTED"
        # Регистрируем событие отклонения
        self.events.append({
            "event": "ListingRejected",
            "listing_id": self.id,
            "reason": reason,
            "occurred_at": datetime.now()
        })

    def mark_as_sold(self):
        """Отметить объявление как проданное"""
        if self.status != "ACTIVE":
            raise ValueError("Можно отметить как проданное только активное объявление")
        self.status = "SOLD"
        # Регистрируем событие продажи
        self.events.append({
            "event": "ListingSold",
            "listing_id": self.id,
            "occurred_at": datetime.now()
        })

    def archive(self):
        """Архивировать объявление"""
        if self.status not in ["ACTIVE", "SOLD"]:
            raise ValueError("Можно архивировать только активное или проданное объявление")
        self.status = "ARCHIVED"
        # Регистрируем событие архивации
        self.events.append({
            "event": "ListingArchived",
            "listing_id": self.id,
            "occurred_at": datetime.now()
        })

    def __eq__(self, other):
        if not isinstance(other, Listing):
            return False
        return self.id == other.id

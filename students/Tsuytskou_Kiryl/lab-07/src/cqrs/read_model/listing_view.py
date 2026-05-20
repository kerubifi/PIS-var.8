from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ListingView:
    """Денормализованная модель для быстрого чтения объявлений"""
    listing_id: str
    seller_id: str
    title: str
    description_preview: str  # Первые 200 символов
    price_amount: float
    price_currency: str
    category_name: str
    status: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_listing(listing):
        return ListingView(
            listing_id=listing.id,
            seller_id=listing.seller_id,
            title=listing.title,
            description_preview=listing.description[:200] + ("..." if len(listing.description) > 200 else ""),
            price_amount=listing.price.amount,
            price_currency=listing.price.currency,
            category_name=listing.category.name,
            status=listing.status,
            created_at=listing.created_at,
            updated_at=listing.updated_at
        )

from dataclasses import dataclass

@dataclass(frozen=True)
class ListingDto:
    listing_id: str
    seller_id: str
    title: str
    description: str
    price_amount: float
    currency: str
    category_name: str
    status: str
    created_at: str

    @staticmethod
    def from_entity(listing):
        return ListingDto(
            listing_id=listing.id,
            seller_id=listing.seller_id,
            title=listing.title,
            description=listing.description,
            price_amount=listing.price.amount,
            currency=listing.price.currency,
            category_name=listing.category.name,
            status=listing.status,
            created_at=listing.created_at.isoformat()
        )

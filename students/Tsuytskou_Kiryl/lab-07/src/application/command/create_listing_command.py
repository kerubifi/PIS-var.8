from dataclasses import dataclass


@dataclass(frozen=True)
class CreateListingCommand:
    title: str
    description: str
    seller_id: str
    price_amount: float
    price_currency: str
    category_name: str

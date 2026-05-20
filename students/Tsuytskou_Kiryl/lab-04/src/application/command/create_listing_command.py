from dataclasses import dataclass

@dataclass(frozen=True)
class CreateListingCommand:
    seller_id: str
    title: str
    description: str
    price_amount: float
    category_name: str
    currency: str = "USD"
    images: list = None

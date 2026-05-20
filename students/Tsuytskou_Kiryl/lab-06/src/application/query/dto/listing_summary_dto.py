from dataclasses import dataclass

@dataclass(frozen=True)
class ListingSummaryDto:
    listing_id: str
    title: str
    price_amount: float
    currency: str
    status: str

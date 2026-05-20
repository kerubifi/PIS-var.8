from dataclasses import dataclass
from typing import Optional, List

@dataclass(frozen=True)
class CreateListingCommand:
    seller_id: str
    title: str
    description: str
    price_amount: float
    category_name: str
    currency: str = "USD"
    images: Optional[List[str]] = None

    def __post_init__(self):
        if not self.title or len(self.title) < 5:
            raise ValueError("Название должно содержать минимум 5 символов")
        if len(self.description) > 5000:
            raise ValueError("Описание не должно превышать 5000 символов")
        if self.price_amount < 0:
            raise ValueError("Цена не может быть отрицательной")

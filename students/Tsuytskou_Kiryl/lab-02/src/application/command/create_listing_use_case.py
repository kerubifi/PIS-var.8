from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.domain.models.price import Price


@dataclass(frozen=True)
class CreateListingCommand:
    """Команда создания объявления"""
    seller_id: str
    title: str
    description: str
    price_amount: float
    price_currency: str = "USD"
    images: list = None


class CreateListingUseCase(ABC):
    """Входящий порт для создания объявления"""
    @abstractmethod
    def create_listing(self, command: CreateListingCommand):
        """Создать новое объявление"""
        pass
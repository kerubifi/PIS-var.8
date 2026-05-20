from dataclasses import dataclass


@dataclass(frozen=True)
class ListingReadDto:
    """Упрощенная модель для отображения пользователю"""
    id: str
    title: str
    seller_name: str
    status: str

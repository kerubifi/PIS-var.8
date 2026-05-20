from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Price:
    """Value Object: Цена объявления с валютой"""
    amount: float
    currency: str = "USD"
    is_free: bool = False

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Цена не может быть отрицательной")
        # Автоматически устанавливаем is_free если цена 0
        object.__setattr__(self, 'is_free', self.amount == 0)

    def __str__(self):
        if self.is_free:
            return "Бесплатно"
        return f"{self.amount} {self.currency}"
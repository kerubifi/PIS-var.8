from dataclasses import dataclass


@dataclass(frozen=True)
class Price:
    """Value Object: Цена объявления (неотрицательная, может быть 0)"""
    amount: float
    currency: str = "RUB"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Цена не может быть отрицательной")
        object.__setattr__(self, 'currency', self.currency.upper().strip() if self.currency else "RUB")

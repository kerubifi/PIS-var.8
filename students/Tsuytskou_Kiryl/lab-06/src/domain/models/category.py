from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Category:
    """Value Object: Категория объявления"""
    name: str
    parent_category: Optional['Category'] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Название категории не может быть пустым")

from dataclasses import dataclass


@dataclass(frozen=True)
class Category:
    """Value Object: Категория объявления"""
    name: str

    def __post_init__(self):
        if not self.name or len(self.name) < 2:
            raise ValueError("Категория должна содержать минимум 2 символа")
        object.__setattr__(self, 'name', self.name.strip())

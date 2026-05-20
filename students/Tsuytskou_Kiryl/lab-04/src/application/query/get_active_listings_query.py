from dataclasses import dataclass

@dataclass(frozen=True)
class GetActiveListingsQuery:
    """Запрос на получение списка активных объявлений с пагинацией"""
    limit: int = 10
    offset: int = 0

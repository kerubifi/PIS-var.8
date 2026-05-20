from dataclasses import dataclass


@dataclass(frozen=True)
class GetListingQuery:
    """Запрос на получение данных объявления по его идентификатору"""
    listing_id: str

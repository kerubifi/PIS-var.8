from dataclasses import dataclass

@dataclass(frozen=True)
class GetListingQuery:
    """Запрос на получение объявления по идентификатору"""
    listing_id: str

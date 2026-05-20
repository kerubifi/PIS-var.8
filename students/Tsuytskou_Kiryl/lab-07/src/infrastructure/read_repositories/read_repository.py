from abc import ABC, abstractmethod
from typing import Optional, List
from src.cqrs.read_model.listing_view import ListingView


class ReadRepository(ABC):
    @abstractmethod
    def save(self, view: ListingView) -> None:
        pass

    @abstractmethod
    def find_by_id(self, listing_id: str) -> Optional[ListingView]:
        pass

    @abstractmethod
    def find_by_status(self, status: str, limit: int = 10, offset: int = 0) -> List[ListingView]:
        pass

    @abstractmethod
    def find_by_seller(self, seller_id: str, limit: int = 10, offset: int = 0) -> List[ListingView]:
        pass

    @abstractmethod
    def find_by_category(self, category_name: str, limit: int = 10, offset: int = 0) -> List[ListingView]:
        pass

    @abstractmethod
    def update_status(self, listing_id: str, status: str) -> None:
        pass

    @abstractmethod
    def update_category(self, listing_id: str, category_name: str) -> None:
        pass

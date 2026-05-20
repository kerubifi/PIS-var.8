from abc import ABC, abstractmethod


class GetListingUseCase(ABC):
    @abstractmethod
    def get_listing(self, listing_id: str):
        """Входящий порт для получения объявления по ID"""
        pass

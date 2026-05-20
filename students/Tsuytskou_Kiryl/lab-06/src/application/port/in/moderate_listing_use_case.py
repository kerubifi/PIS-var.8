from abc import ABC, abstractmethod


class ModerateListingUseCase(ABC):
    @abstractmethod
    def moderate_listing(self, listing_id: str, moderator_id: str, approved: bool, rejection_reason: str = None):
        """Входящий порт для модерации объявления"""
        pass


class GetListingUseCase(ABC):
    @abstractmethod
    def get_listing(self, listing_id: str):
        """Входящий порт для получения объявления по ID"""
        pass

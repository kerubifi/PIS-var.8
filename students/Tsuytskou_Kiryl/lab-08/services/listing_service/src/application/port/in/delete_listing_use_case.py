from abc import ABC, abstractmethod


class DeleteListingUseCase(ABC):
    @abstractmethod
    def delete_listing(self, listing_id: str) -> bool:
        """Входящий порт для удаления объявления"""
        pass

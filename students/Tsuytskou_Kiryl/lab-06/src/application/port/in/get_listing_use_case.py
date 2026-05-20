from abc import ABC, abstractmethod

class GetPostUseCase(ABC):
    @abstractmethod
    def get_post(self, post_id: str):
        """Входящий порт для получения статьи по ID"""
        pass

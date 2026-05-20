from src.infrastructure.adapter.out.in_memory_listing_repository import InMemoryListingRepository
from src.infrastructure.adapter.out.mock_moderation_service import MockModerationService
from src.application.service.listing_service import ListingService

# Mock notification service for demonstration
class MockNotificationService:
    def notify_seller(self, seller_email: str, message: str):
        print(f"[NOTIFICATION] To: {seller_email}")
        print(f"[NOTIFICATION] Message: {message}")

class DependencyContainer:
    """Dependency injection container"""
    def __init__(self):
        self.listing_repository = InMemoryListingRepository()
        self.moderation_service = MockModerationService(auto_approve=True)
        self.notification_service = MockNotificationService()
        self.listing_service = ListingService(
            self.listing_repository,
            self.moderation_service,
            self.notification_service
        )

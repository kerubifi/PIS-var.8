from src.domain.models.listing import Listing
from src.application.command.create_listing_use_case import CreateListingCommand, CreateListingUseCase
from src.application.port.in_.get_listing_use_case import GetListingUseCase
from src.application.port.in_.moderate_listing_use_case import ModerateListingUseCase
from src.application.port.out.listing_repository import ListingRepository
from src.application.port.out.moderation_service import ModerationService
from src.application.port.out.notification_service import NotificationService


class ListingService(CreateListingUseCase, GetListingUseCase, ModerateListingUseCase):
    """Application service (orchestrator) for managing listings"""

    def __init__(self, 
                 listing_repository: ListingRepository,
                 moderation_service: ModerationService,
                 notification_service: NotificationService):
        self.listing_repository = listing_repository
        self.moderation_service = moderation_service
        self.notification_service = notification_service

    def create_listing(self, command: CreateListingCommand):
        """Create a new listing"""
        from src.domain.models.price import Price
        
        price = Price(amount=command.price_amount, currency=command.price_currency)
        listing = Listing(
            listing_id=None,  # Will be set by repository
            seller_id=command.seller_id,
            title=command.title,
            description=command.description,
            price=price,
            images=command.images or []
        )
        
        # Save listing
        saved_listing = self.listing_repository.save(listing)
        
        # Notify seller about new listing for moderation
        self.notification_service.notify_seller(
            seller_email="seller@example.com",  # Placeholder
            message=f"Your listing '{saved_listing.title}' has been sent for moderation"
        )
        
        return saved_listing

    def get_listing(self, listing_id: str):
        """Get listing by ID"""
        return self.listing_repository.find_by_id(listing_id)

    def moderate_listing(self, listing_id: str, moderator_id: str, approved: bool, rejection_reason: str = None):
        """Moderate listing"""
        listing = self.listing_repository.find_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing with ID {listing_id} not found")
        
        # Check content through moderation service
        is_approved, violations = self.moderation_service.check_content(
            listing.title, listing.description
        )
        
        if approved:
            # If moderator approved AND content passed automatic check
            if is_approved:
                listing.approve()
                self.listing_repository.save(listing)
                # Notify seller about approval
                self.notification_service.notify_seller(
                    seller_email="seller@example.com",  # Placeholder
                    message=f"Your listing '{listing.title}' has been approved and published!"
                )
                return True
            else:
                # Content didn't pass automatic check despite moderator approval
                listing.reject(", ".join(violations))
                self.listing_repository.save(listing)
                self.notification_service.notify_seller(
                    seller_email="seller@example.com",  # Placeholder
                    message=f"Your listing '{listing.title}' was rejected due to violations: {', '.join(violations)}"
                )
                return False
        else:
            # Moderator rejected listing
            listing.reject(rejection_reason or "Did not pass moderation")
            self.listing_repository.save(listing)
            self.notification_service.notify_seller(
                seller_email="seller@example.com",  # Placeholder
                message=f"Your listing '{listing.title}' was rejected: {rejection_reason or 'Did not pass moderation'}"
            )
            return False

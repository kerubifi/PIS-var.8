from src.infrastructure.adapter.out.in_memory_listing_repository import InMemoryListingRepository
from src.application.command.handlers.create_listing_handler import CreateListingHandler
from src.application.command.handlers.moderate_listing_handler import ModerateListingHandler
from src.application.query.handlers.get_listing_handler import GetListingHandler
from src.application.service.listing_service import ListingService


class DependencyContainer:
    def __init__(self):
        self.listing_repository = InMemoryListingRepository()
        self.create_handler = CreateListingHandler(self.listing_repository)
        self.moderate_handler = ModerateListingHandler(self.listing_repository)
        self.get_handler = GetListingHandler(self.listing_repository)
        self.listing_service = ListingService(
            self.create_handler,
            self.moderate_handler,
            self.get_handler
        )


container = DependencyContainer()

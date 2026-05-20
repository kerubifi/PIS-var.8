from src.infrastructure.config.database import SessionLocal
from src.infrastructure.adapter.out.listing_controller import SQLAlchemyListingRepository
from src.application.command.handlers.create_listing_handler import CreateListingHandler
from src.application.command.handlers.delete_listing_handler import DeleteListingHandler
from src.application.query.handlers.get_listing_handler import GetListingHandler
from src.application.service.listing_service import ListingService


class DependencyContainer:
    def __init__(self):
        self.db_session = SessionLocal()
        self.listing_repository = SQLAlchemyListingRepository(self.db_session)

        self.create_handler = CreateListingHandler(self.listing_repository)
        self.delete_handler = DeleteListingHandler(self.listing_repository)
        self.get_handler = GetListingHandler(self.listing_repository)

        self.listing_service = ListingService(
            create_handler=self.create_handler,
            delete_handler=self.delete_handler,
            get_handler=self.get_handler
        )

container = DependencyContainer()

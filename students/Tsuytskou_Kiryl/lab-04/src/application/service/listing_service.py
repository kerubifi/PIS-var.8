from src.application.query.get_listing_query import GetListingQuery
from src.application.command.create_listing_command import CreateListingCommand
from src.application.command.moderate_listing_command import ModerateListingCommand
from src.application.command.handlers.create_listing_handler import CreateListingHandler
from src.application.command.handlers.moderate_listing_handler import ModerateListingHandler
from src.application.query.handlers.get_listing_handler import GetListingHandler
from src.application.query.handlers.get_active_listings_handler import GetActiveListingsHandler


class ListingService:
    def __init__(self, create_handler, moderate_handler, get_handler, get_active_handler):
        self.create_handler = create_handler
        self.moderate_handler = moderate_handler
        self.get_handler = get_handler
        self.get_active_handler = get_active_handler

    def create_listing(self, command: CreateListingCommand):
        listing_id = self.create_handler.handle(command)
        return self.get_handler.handle(GetListingQuery(listing_id=listing_id))

    def moderate_listing(self, command: ModerateListingCommand):
        self.moderate_handler.handle(command)

    def get_listing(self, query: GetListingQuery):
        return self.get_handler.handle(query)

    def get_active_listings(self, query):
        return self.get_active_handler.handle(query)

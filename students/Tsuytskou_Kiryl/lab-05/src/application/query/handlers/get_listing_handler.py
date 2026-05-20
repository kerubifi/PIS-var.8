from src.application.query.get_listing_query import GetListingQuery
from src.application.query.dto.listing_dto import ListingDto


class GetListingHandler:
    def __init__(self, listing_repository):
        self.repository = listing_repository

    def handle(self, query: GetListingQuery) -> ListingDto:
        listing = self.repository.find_by_id(query.listing_id)
        if not listing:
            raise ValueError(f"Объявление с ID {query.listing_id} не найдено")
        return ListingDto.from_entity(listing)

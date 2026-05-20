from src.application.query.get_listing_query import GetListingQuery
from src.application.query.dto.listing_read_dto import ListingReadDto


class GetListingHandler:
    def __init__(self, listing_repository):
        self.repository = listing_repository

    def handle(self, query: GetListingQuery) -> ListingReadDto:
        listing = self.repository.find_by_id(query.listing_id)
        if not listing:
            raise ValueError("Объявление не найдено")

        return ListingReadDto(
            id=listing.id,
            title=listing.title,
            seller_name=listing.seller_id,
            status=listing.status
        )

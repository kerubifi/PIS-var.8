from src.application.query.get_active_listings_query import GetActiveListingsQuery
from src.application.query.dto.listing_summary_dto import ListingSummaryDto


class GetActiveListingsHandler:
    def __init__(self, listing_repository):
        self.repository = listing_repository

    def handle(self, query: GetActiveListingsQuery) -> list:
        listings = self.repository.find_by_status("ACTIVE")
        result = []
        start = query.offset
        end = start + query.limit
        for listing in listings[start:end]:
            result.append(ListingSummaryDto(
                listing_id=listing.id,
                title=listing.title,
                price_amount=listing.price.amount,
                currency=listing.price.currency,
                status=listing.status
            ))
        return result

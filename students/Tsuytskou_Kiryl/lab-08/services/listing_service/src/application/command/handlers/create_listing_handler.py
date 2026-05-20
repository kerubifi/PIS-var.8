import uuid
from src.application.command.create_listing_command import CreateListingCommand
from src.domain.models.listing import Listing
from src.domain.models.price import Price
from src.domain.models.category import Category


class CreateListingHandler:
    def __init__(self, listing_repository):
        self.repository = listing_repository

    def handle(self, command: CreateListingCommand) -> str:
        listing_id = str(uuid.uuid4())
        price = Price(amount=command.price_amount, currency=command.price_currency)
        category = Category(name=command.category_name)

        new_listing = Listing(
            listing_id=listing_id,
            seller_id=command.seller_id,
            title=command.title,
            description=command.description,
            price=price,
            category=category
        )

        self.repository.save(new_listing)
        return listing_id

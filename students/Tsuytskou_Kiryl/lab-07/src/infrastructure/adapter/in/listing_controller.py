from src.domain.models.listing import Listing
from src.domain.models.price import Price
from src.domain.models.category import Category


class SQLAlchemyListingRepository:
    def __init__(self, session):
        self.session = session

    def save(self, listing: Listing):
        orm_listing = ListingORM(
            id=listing.id,
            title=listing.title,
            description=listing.description,
            price_amount=listing.price.amount,
            price_currency=listing.price.currency,
            category_name=listing.category.name,
            status=listing.status,
            seller_id=listing.seller_id
        )
        self.session.merge(orm_listing)
        self.session.commit()

    def find_by_id(self, listing_id: str):
        orm_listing = self.session.query(ListingORM).filter(ListingORM.id == listing_id).first()
        if not orm_listing:
            return None
        price = Price(amount=orm_listing.price_amount, currency=orm_listing.price_currency)
        category = Category(name=orm_listing.category_name)
        return Listing(
            listing_id=orm_listing.id,
            seller_id=orm_listing.seller_id,
            title=orm_listing.title,
            description=orm_listing.description,
            price=price,
            category=category
        )

    def delete(self, listing_id: str):
        orm_listing = self.session.query(ListingORM).filter(ListingORM.id == listing_id).first()
        if orm_listing:
            self.session.delete(orm_listing)
            self.session.commit()

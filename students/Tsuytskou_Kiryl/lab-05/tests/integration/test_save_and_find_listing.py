import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.adapter.out.listing_orm import Base, ListingORM
from src.infrastructure.adapter.out.listing_repository_impl import SQLAlchemyListingRepository
from src.domain.models.listing import Listing
from src.domain.models.price import Price
from src.domain.models.category import Category

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def session():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_save_and_find_listing(session):
    repo = SQLAlchemyListingRepository(session)

    price = Price(amount=100.0, currency="USD")
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-123",
        seller_id="seller-1",
        title="Test Listing",
        description="Test Description",
        price=price,
        category=category
    )

    repo.save(listing)
    found = repo.find_by_id("test-123")

    assert found is not None
    assert found.title == "Test Listing"
    assert found.price.amount == 100.0
    assert found.category.name == "Electronics"

    session.close()

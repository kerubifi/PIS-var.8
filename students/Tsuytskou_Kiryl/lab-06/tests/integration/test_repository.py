import pytest
from src.domain.models.listing import Listing
from src.domain.models.price import Price
from src.domain.models.category import Category

from src.infrastructure.adapter.out.in_memory_listing_repository import InMemoryListingRepository


@pytest.fixture
def session():
    repo = InMemoryListingRepository()
    return repo


def test_save_and_find_listing(session):
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

    session.save(listing)
    found = session.find_by_id("test-123")

    assert found is not None
    assert found.title == "Test Listing"
    assert found.price.amount == 100.0
    assert found.category.name == "Electronics"


def test_find_by_status(session):
    price = Price(amount=50.0, currency="USD")
    category = Category(name="Books")
    listing = Listing(
        listing_id="test-456",
        seller_id="seller-1",
        title="Active Listing",
        description="Test description",
        price=price,
        category=category
    )
    listing.approve()
    session.save(listing)

    active = session.find_by_status("ACTIVE")
    assert len(active) >= 1
    assert active[0].title == "Active Listing"


def test_find_by_seller(session):
    price = Price(amount=50.0, currency="USD")
    category = Category(name="Tech")
    listing = Listing(
        listing_id="test-789",
        seller_id="seller-1",
        title="Seller1 Item",
        description="Test description",
        price=price,
        category=category
    )
    session.save(listing)

    found = session.find_by_seller("seller-1")
    assert len(found) >= 1
    assert found[0].seller_id == "seller-1"

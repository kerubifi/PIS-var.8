import pytest
from unittest.mock import MagicMock
from src.cqrs.projection.listing_projection import ListingProjectionHandler
from src.cqrs.read_model.listing_view import ListingView
from src.domain.models.listing import Listing
from src.domain.models.price import Price
from src.domain.models.category import Category


def test_projection_creates_view_on_listing_created():
    """Тест: проекция создаёт View при создании объявления"""
    mock_read_repo = MagicMock()
    handler = ListingProjectionHandler(mock_read_repo)

    price = Price(amount=100.0, currency="USD")
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-1",
        seller_id="seller-1",
        title="Test Listing",
        description="This is a test description for the listing",
        price=price,
        category=category
    )

    handler.on_listing_created(listing)

    mock_read_repo.save.assert_called_once()
    saved_view = mock_read_repo.save.call_args[0][0]
    assert saved_view.listing_id == "test-1"
    assert saved_view.title == "Test Listing"
    assert saved_view.status == "PENDING_MODERATION"


def test_projection_updates_status_on_approve():
    """Тест: проекция обновляет статус при одобрении"""
    mock_read_repo = MagicMock()
    handler = ListingProjectionHandler(mock_read_repo)

    price = Price(amount=100.0)
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-2",
        seller_id="seller-1",
        title="TestAd",
        description="Test description here",
        price=price,
        category=category
    )

    handler.on_listing_approved(listing)
    mock_read_repo.update_status.assert_called_once_with("test-2", "ACTIVE")


def test_projection_updates_status_on_reject():
    """Тест: проекция обновляет статус при отклонении"""
    mock_read_repo = MagicMock()
    handler = ListingProjectionHandler(mock_read_repo)

    price = Price(amount=100.0)
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-3",
        seller_id="seller-1",
        title="TestAd2",
        description="Description for rejection test",
        price=price,
        category=category
    )

    handler.on_listing_rejected(listing)
    mock_read_repo.update_status.assert_called_once_with("test-3", "REJECTED")


def test_projection_creates_preview_correctly():
    """Тест: проекция создаёт превью описания (первые 200 символов)"""
    mock_read_repo = MagicMock()
    handler = ListingProjectionHandler(mock_read_repo)

    price = Price(amount=100.0)
    category = Category(name="Electronics")
    long_description = "x" * 500
    listing = Listing(
        listing_id="test-4",
        seller_id="seller-1",
        title="TestAd3",
        description=long_description,
        price=price,
        category=category
    )

    handler.on_listing_created(listing)

    saved_view = mock_read_repo.save.call_args[0][0]
    assert len(saved_view.description_preview) <= 203  # 200 + "..."
    assert saved_view.description_preview.endswith("...")

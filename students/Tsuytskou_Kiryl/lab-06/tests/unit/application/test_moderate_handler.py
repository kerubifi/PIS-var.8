import pytest
from unittest.mock import MagicMock
from src.application.command.moderate_listing_command import ModerateListingCommand
from src.application.command.handlers.moderate_listing_handler import ModerateListingHandler
from src.application.query.get_listing_query import GetListingQuery
from src.application.query.handlers.get_listing_handler import GetListingHandler


def test_moderate_handler_approve():
    mock_repo = MagicMock()
    mock_listing = MagicMock()
    mock_listing.status = "PENDING_MODERATION"
    mock_repo.find_by_id.return_value = mock_listing

    handler = ModerateListingHandler(mock_repo)
    command = ModerateListingCommand(
        listing_id="test-1",
        moderator_id="mod-1",
        approved=True
    )

    handler.handle(command)
    mock_listing.approve.assert_called_once()
    mock_repo.save.assert_called_once_with(mock_listing)


def test_moderate_handler_reject():
    mock_repo = MagicMock()
    mock_listing = MagicMock()
    mock_listing.status = "PENDING_MODERATION"
    mock_repo.find_by_id.return_value = mock_listing

    handler = ModerateListingHandler(mock_repo)
    command = ModerateListingCommand(
        listing_id="test-1",
        moderator_id="mod-1",
        approved=False,
        rejection_reason="Нарушение правил"
    )

    handler.handle(command)
    mock_listing.reject.assert_called_once_with("Нарушение правил")
    mock_repo.save.assert_called_once_with(mock_listing)


def test_moderate_handler_not_found():
    mock_repo = MagicMock()
    mock_repo.find_by_id.return_value = None

    handler = ModerateListingHandler(mock_repo)
    command = ModerateListingCommand(
        listing_id="missing",
        moderator_id="mod-1",
        approved=True
    )

    with pytest.raises(ValueError, match="не найдено"):
        handler.handle(command)


def test_get_listing_handler_found():
    mock_repo = MagicMock()
    mock_listing = MagicMock()
    mock_listing.id = "listing-1"
    mock_listing.seller_id = "seller-1"
    mock_listing.title = "Test"
    mock_listing.description = "Desc"
    mock_listing.price.amount = 100.0
    mock_listing.price.currency = "USD"
    mock_listing.category.name = "Electronics"
    mock_listing.status = "ACTIVE"
    mock_listing.created_at.isoformat.return_value = "2026-01-01T00:00:00"
    mock_repo.find_by_id.return_value = mock_listing

    handler = GetListingHandler(mock_repo)
    result = handler.handle(GetListingQuery(listing_id="listing-1"))

    assert result.listing_id == "listing-1"
    assert result.title == "Test"
    mock_repo.find_by_id.assert_called_once_with("listing-1")


def test_get_listing_handler_not_found():
    mock_repo = MagicMock()
    mock_repo.find_by_id.return_value = None

    handler = GetListingHandler(mock_repo)

    with pytest.raises(ValueError, match="не найдено"):
        handler.handle(GetListingQuery(listing_id="missing"))

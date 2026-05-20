import pytest
from unittest.mock import MagicMock
from src.application.command.moderate_listing_command import ModerateListingCommand
from src.application.command.handlers.moderate_listing_handler import ModerateListingHandler


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

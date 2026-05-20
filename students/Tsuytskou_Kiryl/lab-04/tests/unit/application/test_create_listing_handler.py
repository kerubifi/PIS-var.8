import pytest
from unittest.mock import MagicMock
from src.application.command.create_listing_command import CreateListingCommand
from src.application.command.handlers.create_listing_handler import CreateListingHandler


def test_create_listing_handler_success():
    mock_repo = MagicMock()
    handler = CreateListingHandler(mock_repo)
    command = CreateListingCommand(
        seller_id="seller-1",
        title="Test Listing",
        description="Test Description",
        price_amount=100.0,
        category_name="Electronics"
    )

    listing_id = handler.handle(command)

    assert listing_id is not None
    mock_repo.save.assert_called_once()


def test_create_listing_handler_invalid_title():
    mock_repo = MagicMock()
    handler = CreateListingHandler(mock_repo)

    with pytest.raises(ValueError, match="Название должно содержать минимум 5 символов"):
        command = CreateListingCommand(
            seller_id="seller-1",
            title="Hi",
            description="Test Description",
            price_amount=100.0,
            category_name="Electronics"
        )
        handler.handle(command)


def test_create_listing_handler_invalid_description():
    mock_repo = MagicMock()
    handler = CreateListingHandler(mock_repo)

    with pytest.raises(ValueError, match="Описание не должно превышать 5000 символов"):
        command = CreateListingCommand(
            seller_id="seller-1",
            title="Valid Title",
            description="x" * 5001,
            price_amount=100.0,
            category_name="Electronics"
        )
        handler.handle(command)

import pytest
from unittest.mock import MagicMock
from src.application.query.handlers.get_active_listings_handler import GetActiveListingsHandler
from src.application.query.get_active_listings_query import GetActiveListingsQuery


def test_get_active_listings_handler():
    mock_repo = MagicMock()
    mock_listing1 = MagicMock()
    mock_listing1.id = "l1"
    mock_listing1.title = "Item1"
    mock_listing1.price.amount = 50.0
    mock_listing1.price.currency = "USD"
    mock_listing1.status = "ACTIVE"
    mock_listing2 = MagicMock()
    mock_listing2.id = "l2"
    mock_listing2.title = "Item2"
    mock_listing2.price.amount = 0.0
    mock_listing2.price.currency = "USD"
    mock_listing2.status = "SOLD"

    mock_repo.find_by_status.return_value = [mock_listing1, mock_listing2]

    handler = GetActiveListingsHandler(mock_repo)
    result = handler.handle(GetActiveListingsQuery(limit=10, offset=0))

    assert len(result) == 2
    assert result[0].listing_id == "l1"
    assert result[0].status == "ACTIVE"
    assert result[1].listing_id == "l2"
    mock_repo.find_by_status.assert_called_once_with("ACTIVE")

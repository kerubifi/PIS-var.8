import pytest
from src.domain.models.listing import Listing
from src.domain.models.price import Price
from src.domain.models.category import Category
from src.domain.exceptions.domain_exception import ListingValidationError, InvalidListingStateError


def test_listing_title_validation():
    """Тест: название < 5 символов должно вызывать ошибку"""
    price = Price(amount=100.0)
    category = Category(name="Electronics")
    with pytest.raises(ValueError, match="Название должно содержать минимум 5 символов"):
        Listing(
            listing_id="test-1",
            seller_id="seller-1",
            title="Hi",
            description="Valid description",
            price=price,
            category=category
        )


def test_listing_description_validation():
    """Тест: описание > 5000 символов должно вызывать ошибку"""
    price = Price(amount=100.0)
    category = Category(name="Electronics")
    long_desc = "x" * 5001
    with pytest.raises(ValueError, match="Описание не должно превышать 5000 символов"):
        Listing(
            listing_id="test-2",
            seller_id="seller-1",
            title="Valid Title",
            description=long_desc,
            price=price,
            category=category
        )


def test_listing_price_validation():
    """Тест: отрицательная цена вызывает ошибку"""
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        Price(amount=-10.0)


def test_listing_free_price():
    """Тест: цена 0 означает бесплатно"""
    price = Price(amount=0.0)
    assert price.is_free == True
    assert str(price) == "Бесплатно"


def test_listing_approve_success():
    """Тест: одобрение меняет статус с PENDING_MODERATION на ACTIVE"""
    price = Price(amount=100.0)
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-3",
        seller_id="seller-1",
        title="Test Listing",
        description="Test description",
        price=price,
        category=category
    )
    assert listing.status == "PENDING_MODERATION"
    listing.approve()
    assert listing.status == "ACTIVE"
    assert len(listing.events) == 1
    assert listing.events[0]["event"] == "ListingApproved"


def test_listing_reject_success():
    """Тест: отклонение меняет статус на REJECTED"""
    price = Price(amount=100.0)
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-4",
        seller_id="seller-1",
        title="Test Listing",
        description="Test description",
        price=price,
        category=category
    )
    listing.reject("Нарушение правил")
    assert listing.status == "REJECTED"
    assert len(listing.events) == 1
    assert listing.events[0]["event"] == "ListingRejected"


def test_listing_mark_as_sold():
    """Тест: продажа меняет статус на SOLD"""
    price = Price(amount=100.0)
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-5",
        seller_id="seller-1",
        title="Test Listing",
        description="Test description",
        price=price,
        category=category
    )
    listing.approve()
    listing.mark_as_sold()
    assert listing.status == "SOLD"
    assert len(listing.events) == 2
    assert listing.events[1]["event"] == "ListingSold"


def test_listing_archive():
    """Тест: архивация меняет статус на ARCHIVED"""
    price = Price(amount=100.0)
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-6",
        seller_id="seller-1",
        title="Test Listing",
        description="Test description",
        price=price,
        category=category
    )
    listing.approve()
    listing.mark_as_sold()
    listing.archive()
    assert listing.status == "ARCHIVED"
    assert listing.events[2]["event"] == "ListingArchived"


def test_cannot_approve_non_pending():
    """Тест: нельзя одобрить не находящееся на модерации объявление"""
    price = Price(amount=100.0)
    category = Category(name="Electronics")
    listing = Listing(
        listing_id="test-7",
        seller_id="seller-1",
        title="Test Listing",
        description="Test description",
        price=price,
        category=category
    )
    listing.approve()
    with pytest.raises(InvalidListingStateError, match="Можно одобрить только объявление на модерации"):
        listing.approve()


def test_category_creation():
    """Тест: создание категории"""
    category = Category(name="Electronics")
    assert category.name == "Electronics"
    with pytest.raises(ValueError, match="Название категории не может быть пустым"):
        Category(name="")

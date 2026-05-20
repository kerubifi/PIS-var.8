import pytest
from src.domain.models.listing import Listing
from src.domain.models.price import Price


def test_listing_title_validation():
    """Тест: название < 5 символов должно вызывать ошибку"""
    price = Price(amount=10.0)
    with pytest.raises(ValueError, match="Название должно содержать минимум 5 символов"):
        Listing(
            listing_id="test-1",
            seller_id="seller-1",
            title="Hi",  # Только 2 символа
            description="Valid description",
            price=price
        )


def test_listing_description_validation():
    """Тест: описание > 5000 символов должно вызывать ошибку"""
    price = Price(amount=10.0)
    long_description = "x" * 5001
    with pytest.raises(ValueError, match="Описание не должно превышать 5000 символов"):
        Listing(
            listing_id="test-2",
            seller_id="seller-1",
            title="Valid Title",
            description=long_description,
            price=price
        )


def test_listing_approve_changes_status():
    """Тест смены статуса при одобрении"""
    price = Price(amount=50.0)
    listing = Listing(
        listing_id="test-3",
        seller_id="seller-1",
        title="Test Item",
        description="A test item for sale",
        price=price
    )

    listing.approve()
    assert listing.status == "ACTIVE"
    assert len(listing.events) > 0


def test_listing_reject_changes_status():
    """Тест: отклонение меняет статус на REJECTED"""
    price = Price(amount=50.0)
    listing = Listing(
        listing_id="test-4",
        seller_id="seller-1",
        title="Test Item",
        description="A test item for sale",
        price=price
    )
    
    listing.reject("Нарушение правил")
    assert listing.status == "REJECTED"
    assert len(listing.events) > 0


def test_listing_mark_as_sold_changes_status():
    """Тест: продажа меняет статус на SOLD"""
    price = Price(amount=50.0)
    listing = Listing(
        listing_id="test-5",
        seller_id="seller-1",
        title="Test Item",
        description="A test item for sale",
        price=price
    )
    
    listing.approve()
    listing.mark_as_sold()
    assert listing.status == "SOLD"
    assert len(listing.events) == 2  # approve + sold


def test_listing_archive_changes_status():
    """Тест: архивация меняет статус на ARCHIVED"""
    price = Price(amount=50.0)
    listing = Listing(
        listing_id="test-6",
        seller_id="seller-1",
        title="Test Item",
        description="A test item for sale",
        price=price
    )
    
    listing.approve()
    listing.mark_as_sold()
    listing.archive()
    assert listing.status == "ARCHIVED"
    assert len(listing.events) == 3


def test_cannot_approve_non_pending_listing():
    """Тест: нельзя одобрить не находящееся на модерации объявление"""
    price = Price(amount=50.0)
    listing = Listing(
        listing_id="test-7",
        seller_id="seller-1",
        title="Test Item",
        description="A test item for sale",
        price=price
    )
    
    listing.approve()  # стало ACTIVE
    
    with pytest.raises(ValueError, match="Можно одобрить только объявление на модерации"):
        listing.approve()  # повторная попытка


def test_price_negative_raises_error():
    """Тест: отрицательная цена вызывает ошибку"""
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        Price(amount=-10.0)


def test_price_zero_is_free():
    """Тест: цена 0 означает бесплатно"""
    price = Price(amount=0.0)
    assert price.is_free == True
    assert str(price) == "Бесплатно"


def test_category_creation():
    """Тест: создание категории"""
    from src.domain.models.category import Category
    
    category = Category(name="Electronics")
    assert category.name == "Electronics"
    
    with pytest.raises(ValueError, match="Название категории не может быть пустым"):
        Category(name="")
import pytest
from src.domain.models.listing import Listing
from src.domain.models.price import Price
from src.domain.models.category import Category


def test_listing_creation():
    """Тест создания объявления"""
    price = Price(amount=100.0, currency="USD")
    listing = Listing(
        listing_id="test-1",
        seller_id="seller-1",
        title="Test Listing",
        description="This is a test description",
        price=price
    )
    
    assert listing.id == "test-1"
    assert listing.seller_id == "seller-1"
    assert listing.title == "Test Listing"
    assert listing.description == "This is a test description"
    assert listing.price == price
    assert listing.status == "PENDING_MODERATION"


def test_listing_creation_with_free_price():
    """Тест создания бесплатного объявления"""
    price = Price(amount=0.0, currency="USD")
    listing = Listing(
        listing_id="test-free",
        seller_id="seller-1",
        title="Free Item",
        description="This item is free",
        price=price
    )
    
    assert listing.price.is_free == True
    assert str(listing.price) == "Бесплатно"


def test_listing_approve():
    """Тест одобрения объявления"""
    price = Price(amount=50.0)
    listing = Listing(
        listing_id="test-2",
        seller_id="seller-1",
        title="Test Item",
        description="A test item for sale",
        price=price
    )
    
    # Изначально должно быть на модерации
    assert listing.status == "PENDING_MODERATION"
    
    # Одобряем объявление
    listing.approve()
    assert listing.status == "ACTIVE"


def test_listing_reject():
    """Тест отклонения объявления"""
    price = Price(amount=75.0)
    listing = Listing(
        listing_id="test-3",
        seller_id="seller-1",
        title="Test Item",
        description="A test item for sale",
        price=price
    )
    
    listing.reject("Нарушение правил размещения")
    assert listing.status == "REJECTED"


def test_listing_mark_as_sold():
    """Тест отметки объявления как проданного"""
    price = Price(amount=120.0)
    listing = Listing(
        listing_id="test-4",
        seller_id="seller-1",
        title="Sold Item",
        description="This item was sold",
        price=price
    )
    
    # Сначала одобряем
    listing.approve()
    assert listing.status == "ACTIVE"
    
    # Затем отмечаем как проданное
    listing.mark_as_sold()
    assert listing.status == "SOLD"


def test_listing_archive():
    """Тест архивации объявления"""
    price = Price(amount=200.0)
    listing = Listing(
        listing_id="test-5",
        seller_id="seller-1",
        title="Archived Item",
        description="This item is archived",
        price=price
    )
    
    # Одобряем и продаем
    listing.approve()
    listing.mark_as_sold()
    assert listing.status == "SOLD"
    
    # Архивируем
    listing.archive()
    assert listing.status == "ARCHIVED"


def test_listing_title_validation():
    """Тест валидации названия объявления"""
    price = Price(amount=10.0)
    
    # Название слишком короткое
    with pytest.raises(ValueError, match="Название должно содержать минимум 5 символов"):
        Listing(
            listing_id="test-6",
            seller_id="seller-1",
            title="Hi",  # Только 2 символа
            description="Valid description",
            price=price
        )


def test_listing_description_validation():
    """Тест валидации описания объявления"""
    price = Price(amount=10.0)
    
    # Описание слишком длинное (> 5000 символов)
    long_description = "x" * 5001
    with pytest.raises(ValueError, match="Описание не должно превышать 5000 символов"):
        Listing(
            listing_id="test-7",
            seller_id="seller-1",
            title="Valid Title",
            description=long_description,
            price=price
        )


def test_price_validation():
    """Тест валидации цены"""
    # Отрицательная цена должна вызывать ошибку
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        Price(amount=-10.0, currency="USD")


def test_price_is_free():
    """Тест определения бесплатной цены"""
    free_price = Price(amount=0.0, currency="USD")
    paid_price = Price(amount=5.0, currency="USD")
    
    assert free_price.is_free == True
    assert paid_price.is_free == False
    assert str(free_price) == "Бесплатно"
    assert str(paid_price) == "5.0 USD"


def test_category_creation():
    """Тест создания категории"""
    category = Category(name="Electronics")
    assert category.name == "Electronics"
    assert category.parent_category is None
    
    # Категория с родителем
    parent = Category(name="Electronics")
    child = Category(name="Smartphones", parent_category=parent)
    assert child.name == "Smartphones"
    assert child.parent_category == parent
    
    # Пустое название категории
    with pytest.raises(ValueError, match="Название категории не может быть пустым"):
        Category(name="")


def test_category_with_parent():
    """Тест создания иерархии категорий"""
    electronics = Category(name="Electronics")
    smartphones = Category(name="Smartphones", parent_category=electronics)
    iphones = Category(name="iPhones", parent_category=smartphones)
    
    assert iphones.parent_category.name == "Smartphones"
    assert iphones.parent_category.parent_category.name == "Electronics"
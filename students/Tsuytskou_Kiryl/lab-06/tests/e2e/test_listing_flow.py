from fastapi.testclient import TestClient
from src.infrastructure.adapter.in_.listing_controller import app

client = TestClient(app)


def test_full_listing_flow():
    """E2E сценарий: создание объявления → одобрение → проверка статуса ACTIVE"""

    # 1. Создание объявления через API (JSON body)
    response = client.post(
        "/api/listings",
        json={
            "seller_id": "seller-1",
            "title": "Test Listing",
            "description": "Test description",
            "price_amount": 100.0,
            "category_name": "Electronics"
        }
    )
    
    # Добавим отладку
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
    
    assert response.status_code == 200, f"Error: {response.text}"
    listing_id = response.json().get("listing_id")
    assert listing_id is not None

    # 2. Проверка статуса после создания (должен быть PENDING_MODERATION)
    response = client.get(f"/api/listings/{listing_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "PENDING_MODERATION"

    # 3. Одобрение объявления модератором
    response = client.post(f"/api/listings/{listing_id}/approve?moderator_id=mod-1")
    assert response.status_code == 200
    assert response.json()["status"] == "approved"

    # 4. Проверка, что статус изменился на ACTIVE
    response = client.get(f"/api/listings/{listing_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "ACTIVE"


def test_full_listing_reject_flow():
    """E2E сценарий: создание объявления → отклонение → проверка статуса REJECTED"""

    # 1. Создание объявления через API (JSON body)
    response = client.post(
        "/api/listings",
        json={
            "seller_id": "seller-1",
            "title": "Test Listing 2",
            "description": "Test description",
            "price_amount": 100.0,
            "category_name": "Electronics"
        }
    )
    
    if response.status_code != 200:
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
    
    assert response.status_code == 200, f"Error: {response.text}"
    listing_id = response.json().get("listing_id")
    assert listing_id is not None

    # 2. Отклонение объявления модератором
    response = client.post(
        f"/api/listings/{listing_id}/reject",
        params={"moderator_id": "mod-1", "rejection_reason": "Нарушение правил"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"

    # 3. Проверка, что статус изменился на REJECTED
    response = client.get(f"/api/listings/{listing_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "REJECTED"
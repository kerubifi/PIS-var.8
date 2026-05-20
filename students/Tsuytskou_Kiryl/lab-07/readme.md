<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">"Брестский Государственный технический университет"</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №7</strong></p>
<p align="center"><strong>По дисциплине:</strong> "Проектирование интернет-систем"</p>
<p align="center"><strong>Тема:</strong> "CQRS и Read Models"</p>
<br><br><br><br><br><br>
<p align="right"><strong>Выполнил:</strong></p>
<p align="right">Студент 3 курса</p>
<p align="right">Группа ПО-13</p>
<p align="right">Тютьков К. О.</p>
<p align="right"><strong>Проверил:</strong></p>
<p align="right">Шорох Д. В.</p>
<br><br><br><br><br>
<p align="center"><strong>Брест 2026</strong></p>

---


## Вариант №8 - Объявки «Бери, пока горячее»

**Питч:** _От велосипеда до учебника - всё тут_

**Ядро домена:** _Объявления, Категории, Цены, Модерация, Статусы_- _Объявки «Бери, пока горячее»_

---


## Цель работы

Реализовать CQRS с разделением Write Model и Read Model.

---


## Ход выполнения работы

### 1. Write Model — Агрегат Listing

**Агрегат:** _Listing (Объявление)_

**Value Objects:** _Price_ (≥0, может быть 0), _Category_

**Структура:**

- Инварианты:
   - Заголовок объявления минимум 5 символов
   - Описание не более 5000 символов
   - Цена неотрицательна (Price ≥ 0)

- Статусы жизненного цикла:
   - `PENDING_MODERATION` — на модерации
   - `ACTIVE` — активно
   - `REJECTED` — отклонено модерацией
   - `SOLD` — продано
   - `ARCHIVED` — в архиве

---


### 2. Read Model — ListingView

**Проекция:** _ListingView (денормализованная для быстрого чтения)_

**Структура:**

- Денормализованная таблица / in-memory store с полями:
  - `listing_id`, `seller_id`, `title`, `description_preview` (первые 200 символов),
    `price_amount`, `price_currency`, `category_name`, `status`, `created_at`, `updated_at`

- `description_preview` строится автоматически через `ListingView.from_listing()`

- Избавление от JOIN при чтении списка объявлений — все нужные данные уже лежат в одном месте

---


### 3. Event-Driven Sync — События домена

**События:**

- `ListingCreated` → `on_listing_created()` — создать запись в Read Model
- `ListingApproved` → `on_listing_approved()` — обновить статус на ACTIVE
- `ListingRejected` → `on_listing_rejected()` — обновить статус на REJECTED
- `ListingSold` → `on_listing_sold()` — обновить статус на SOLD
- `ListingArchived` → `on_listing_archived()` — обновить статус на ARCHIVED
- `CategoryUpdated` → `on_category_updated()` — массовое обновление категорий в Read Model

**Проектор:** _ListingProjectionHandler_

Отвечает за преобразование доменных событий в изменения Read Model. Все операции с Read Repository абстрагированы через интерфейс `ReadRepository`.

---


### 4. Архитектура проекта

```
lab-07/src/
├── domain/
│   ├── exceptions/domain_exception.py   # DomainException, InvalidListingStateError
│   └── models/
│       ├── listing.py                   # Aggregate Root
│       ├── price.py                     # Value Object: цена (≥ 0)
│       └── category.py                  # Value Object: категория
├── application/
│   ├── command/
│   │   ├── create_listing_command.py
│   │   ├── delete_listing_command.py
│   │   └── handlers/
│   │       ├── create_listing_handler.py
│   │       └── delete_listing_handler.py
│   ├── query/
│   │   ├── get_listing_query.py
│   │   ├── dto/listing_read_dto.py
│   │   └── handlers/get_listing_handler.py
│   ├── port/in/
│   │   ├── get_listing_use_case.py
│   │   └── delete_listing_use_case.py
│   └── service/listing_service.py
├── cqrs/
│   ├── projection/listing_projection.py      # ListingProjectionHandler
│   └── read_model/listing_view.py            # ListingView
├── infrastructure/
│   ├── adapter/in/listing_controller.py      # SQLAlchemyListingRepository
│   ├── config/
│   │   ├── database.py
│   │   ├── dependency_injection.py
│   │   └── read_repository.py                # ReadRepository ABC
│   └── docker-compose.yml
└── requirements.txt
```

---


### 5. Тесты проекций (tests/test_projection.py)

Всего 4 теста, все проходят:

| Тест | Что проверяется |
|------|-----------------|
| `test_projection_creates_view_on_listing_created` | При `on_listing_created()` вызывается `save()` с корректным `ListingView` |
| `test_projection_updates_status_on_approve` | При `on_listing_approved()` вызывается `update_status(id, "ACTIVE")` |
| `test_projection_updates_status_on_reject` | При `on_listing_rejected()` вызывается `update_status(id, "REJECTED")` |
| `test_projection_creates_preview_correctly` | `description_preview` не длиннее 203 симв. и заканчивается на `...` |

---


## Таблица критериев оценки

| Критерий | Баллы | Выполнено |
|----------|-------|-----------|
| Write Model | 20 | ✅ |
| Read Model | 25 | ✅ |
| Event-Driven Sync | 25 | ✅ |
| Оптимизация запросов | 15 | ✅ |
| Тесты проекций | 10 | ✅ |
| Качество документации | 5 | ✅ |
| **ИТОГО** | **100** | |

---


## Вывод

✍️ В рамках лабораторной работы реализована архитектура CQRS для системы объявлений «Бери, пока горячее». Write Model представляет собой нормализованную структуру таблиц, где каждый агрегат (Listing) хранит своё состояние и обеспечивает соблюдение бизнес-инвариантов (мин. 5 символов в заголовке, цена ≥ 0). Read Model — денормализованный `ListingView` с предзагруженными полями, что позволяет избежать JOIN при чтении списка объявлений. Синхронизация между моделями осуществляется через `ListingProjectionHandler`, который реагирует на доменные события `ListingCreated`, `ListingApproved`, `ListingRejected`, `ListingSold`, `ListingArchived`. Все компоненты покрыты тестами, все 4 теста проходят успешно.

---


**Дата выполнения:** _19.05.2026_  
**Оценка:** _____________  
**Подпись преподавателя:** _____________

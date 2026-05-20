<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">"Брестский Государственный технический университет"</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №9</strong></p>
<p align="center"><strong>По дисциплине:</strong> "Проектирование интернет-систем"</p>
<p align="center"><strong>Тема:</strong> "Protocol Buffers и gRPC"</p>
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

Изучить Protocol Buffers и gRPC для высокопроизводительной связи между микросервисами.

---


## Ход выполнения работы

### 1. listing.proto — Протокол для сервиса объявлений

```protobuf
syntax = "proto3";
package listing;

service ListingService {
  rpc CreateListing  (CreateListingRequest)  returns (CreateListingResponse);
  rpc GetListing     (GetListingRequest)     returns (GetListingResponse);
  rpc ApproveListing (ApproveListingRequest) returns (ApproveListingResponse);
  rpc RejectListing  (RejectListingRequest)  returns (RejectListingResponse);
  rpc ListListings   (ListListingsRequest)   returns (ListListingsResponse);
  rpc StreamNewListings (Empty) returns (stream Listing); // Server-side streaming
}
```
Сообщение `Listing` содержит: `id, seller_id, title, description, price_amount, price_currency, category_name, status, created_at`.

---


### 2. category.proto — Протокол для сервиса категорий

```protobuf
syntax = "proto3";
package category;

service CategoryService {
  rpc CreateCategory  (CreateCategoryRequest)  returns (CreateCategoryResponse);
  rpc GetCategory     (GetCategoryRequest)     returns (GetCategoryResponse);
  rpc ListCategories  (ListCategoriesRequest)  returns (ListCategoriesResponse);
}
```

---


### 3. moderation.proto — Протокол для сервиса модерации

```protobuf
syntax = "proto3";
package moderation;

service ModerationService {
  rpc ListModerationListings (ListModerationListingsRequest) returns (ListModerationListingsResponse);
  rpc ApproveModeration      (ApproveModerationRequest)      returns (ApproveModerationResponse);
  rpc RejectModeration       (RejectModerationRequest)       returns (RejectModerationResponse);
}
```

---


### 4. gRPC сервер (ListingService)

**Реализация:** `services/listing_service/src/grpc_server.py`

- `ListingServiceServicer` — обработчик всех 6 RPC-методов
- Валидация на стороне сервера: заголовок ≥5 символов, описание ≤5000, цена ≥0
- `InMemoryRepository` для демонстрации (в проде — ListinggreSQL)
- Порт gRPC: **50051**

---


### 5. gRPC клиент (grpc_client_test.py)

6 тестов:
| № | Тест | Ожидаемый результат |
|---|------|---------------------|
| 1 | `CreateListing` (валидный) | 200-подобный ответ с ID и статусом PENDING_MODERATION |
| 2 | `GetListing` по ID | Объявление найдено |
| 3 | `ApproveListing` | Статус изменён на ACTIVE |
| 4 | `GetListing` после approve | Статус = ACTIVE |
| 5 | `CreateListing` с коротким названием | `INVALID_ARGUMENT` от сервера |
| 6 | `StreamNewListings` | Получено 10 потоковых сообщений с интервалом 2 сек |

---


### 6. Сравнение REST ↔ gRPC

| Параметр | REST (Лаба 8) | gRPC (Лаба 9) |
|----------|--------------|--------------|
| Формат | JSON | Protocol Buffers (бинарный) |
| Протокол | HTTP/1.1 | HTTP/2 |
| Contract | Отсутствует | `.proto` файл (строгий контракт) |
| Streaming | Нет | ✅ Server-side / Bidirectional |
| Размер данных | Крупный | Компактный (бинарный) |
| Типизация | Нестрогая | Строгая (генерируется код) |
| Кроссплатформенность | Высокая | Высокая (генерируется под любой язык) |

---


## Таблица критериев оценки

| Критерий | Баллы | Выполнено |
|----------|-------|-----------|
| listing.proto | 15 | ✅ |
| category.proto | 10 | ✅ |
| moderation.proto | 10 | ✅ |
| gRPC сервер (6 методов) | 25 | ✅ |
| gRPC клиент (6 тестов) | 20 | ✅ |
| Сравнение REST ↔ gRPC | 10 | ✅ |
| Качество документации | 10 | ✅ |
| **ИТОГО** | **100** | |

---


## Вывод

✍️ В рамках лабораторной работы реализованы три gRPC-сервиса для системы объявлений «Бери, пока горячее»: `ListingService` (6 RPC-методов, включая server-side streaming `StreamNewListings`), `CategoryService` (CRUD категорий), `ModerationService` (модерация объявлений). Контракты описаны в `.proto`-файлах (`listing.proto`, `category.proto`, `moderation.proto`), из которых автоматически генерируется типобезопасный код на Python. Библиотека `grpcio` обеспечивает взаимодействие по HTTP/2 в бинарном формате Protocol Buffers, что даёт преимущества по сравнению с REST+JSON: компактный размер данных, строгий контракт и нативная поддержка стриминга. В отличие от Лабы 8, где коммуникация между сервисами шла через асинхронный RabbitMQ, здесь общение синхронное и типизированное, что упрощает отладку и гарантирует совместимость клиента и сервера на уровне компиляции. Все 6 тестов клиента проходят успешно.

---


**Дата выполнения:** _19.05.2026_  
**Оценка:** _____________  
**Подпись преподавателя:** _____________

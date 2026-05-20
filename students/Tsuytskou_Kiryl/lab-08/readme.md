<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">"Брестский Государственный технический университет"</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №8</strong></p>
<p align="center"><strong>По дисциплине:</strong> "Проектирование интернет-систем"</p>
<p align="center"><strong>Тема:</strong> "Микросервисы и Event Bus"</p>
<br><br><br><br><br><br>
<p align="right"><strong>Выполнил:</strong></p>
<p align="right">Студент 3 курса</p>
<p align="right">Группа ______</p>
<p align="right">_[ваше ФИО]_</p>
<p align="right"><strong>Проверил:</strong></p>
<p align="right">Шорох Д. В.</p>
<br><br><br><br><br>
<p align="center"><strong>Брест 2026</strong></p>

---


## Вариант №8 - Объявки «Бери, пока горячее»

**Питч:** _От велосипеда до учебника - всё тут_

**Ядро домена:** _Объявления, Категории, Цены, Модерация, Статусы_- _Объявки «Бери, пока горячее»_

---


## Ход выполнения работы

### 1. Listing Service
**Bounded Context:** _Объявления, Цены, Статусы_

**Агрегат:** _Listing_ с Value Objects `Price` (≥0) и `Category`
**Статусы:** `PENDING_MODERATION → ACTIVE → SOLD / ARCHIVED / REJECTED`

**API:**
- `POST /api/listings` — создать объявление
- `GET /api/listings/{id}` — получить объявление по ID
- `GET /api/listings` — список объявлений (фильтр по статусу)
- `POST /api/listings/{id}/approve` — одобрить объявление

**События:** `ListingCreated`, `ListingApproved`, `ListingRejected`

---

### 2. Category Service
**Bounded Context:** _Категории_

**API:**
- `POST /api/categories` — создать категорию
- `GET /api/categories` — список категорий
- `GET /api/categories/{id}` — получить категорию по ID

**События:** `CategoryCreated`

---

### 3. Moderation Service
**Bounded Context:** _Модерация_

Слушает события из `listing_events` exchange:
- `listing.created` → логирует новое объявление на проверку
- `listing.approved` → логирует одобрение
- `listing.rejected` → логирует отклонение
- `category.created` → логирует создание категории

---

### 4. Event Bus (RabbitMQ)
**Exchange:** `listing_events` (topic)

**События:**
| Событие | Routing Key | Публикует |
|---------|-------------|-----------|
| `ListingCreated` | `listing.created` | listing_service |
| `ListingApproved` | `listing.approved` | listing_service |
| `ListingRejected` | `listing.rejected` | listing_service |
| `CategoryCreated` | `category.created` | category_service |

**Слушатели:**
- `moderation_service` — все 4 ключа
- `notification_service` (неimplemented) — одобрение/отклонение/создание

---

### 5. API Gateway (nginx)
**Маршрутизация:**
- `/api/listings/**` → `listing_service:8000`
- `/api/categories/**` → `category_service:8000`
- `/api/moderation/**` → `moderation_service:8000`

```nginx
worker_processes 1;

events { worker_connections 1024; }

http {
    server {
        listen 80;

        location /api/listings {
            proxy_pass http://listing_service:8000;
        }
        location /api/categories {
            proxy_pass http://category_service:8000;
        }
        location /api/moderation {
            proxy_pass http://moderation_service:8000;
        }
    }
}
```

---

### 6. Docker Compose
**Сервисы:**
| Сервис | Порт | Назначение |
|--------|------|------------|
| `rabbitmq` | 5672, 15672 | Шина событий + админка |
| `listing_service` | 8001 | CRUD объявлений + публикация событий |
| `category_service` | 8002 | CRUD категорий + публикация событий |
| `moderation_service` | 8003 | Consumer модерации |
| `gateway` | 80 | nginx API Gateway |
| `db` | 5432 | PostgreSQL `listing_db` |

---

## Таблица критериев оценки

| Критерий | Баллы | Выполнено |
|----------|-------|-----------|
| Listing Service: bounded context | 15 | ✅ |
| Category Service: CRUD | 15 | ✅ |
| Moderation Service: bounded context | 10 | ✅ |
| Event Bus: RabbitMQ | 25 | ✅ |
| API Gateway | 15 | ✅ |
| Docker Compose | 10 | ✅ |
| Качество документации | 10 | ✅ |
| **ИТОГО** | **100** | |

---


## Вывод

✍️ В ходе выполнения лабораторной работы система объявлений «Бери, пока горячее» была разбита на микросервисы с асинхронной коммуникацией через Event Bus (RabbitMQ, exchange `listing_events`). `Listing Service` управляет жизненным циклом объявлений и публикует доменные события при смене статуса. `Category Service` управляет категориями и публикует `CategoryCreated`. `Moderation Service` потребляет все события для логирования модерации. API Gateway (nginx) предоставляет единую точку входа и маршрутизирует запросы по сервисам. Все компоненты упакованы в Docker-контейнеры и управляются через `docker-compose.yml`. Архитектура обеспечивает слабую связанность между сервисами, возможность независимого масштабирования и отказоустойчивость через асинхронную обработку событий.

---


**Дата выполнения:** _19.05.2026_  
**Оценка:** _____________  
**Подпись преподавателя:** _____________

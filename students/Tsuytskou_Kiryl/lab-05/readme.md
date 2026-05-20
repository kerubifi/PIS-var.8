<p align="center">Министерство образования Республики Беларусь</p>
<p align="center">Учреждение образования</p>
<p align="center">"Брестский Государственный технический университет"</p>
<p align="center">Кафедра ИИТ</p>
<br><br><br><br><br><br>
<p align="center"><strong>Лабораторная работа №5</strong></p>
<p align="center"><strong>По дисциплине:</strong> "Проектирование интернет-систем"</p>
<p align="center"><strong>Тема:</strong> "Infrastructure Layer: Repository, REST API, БД"</p>
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

Реализовать инфраструктурный слой с адаптерами для портов (Repository, REST Controller) с использованием SQLAlchemy и PostgreSQL.

---


## Ход выполнения работы

### 1. Repository (PostgreSQL)

**Реализованные методы:**

- `save(listing)` - сохранение объявления (UPSERT через merge)
- `find_by_id(listing_id)` - поиск по ID
- `find_by_status(status)` - поиск по статусу (ACTIVE, SOLD и т.д.)
- `find_by_seller(seller_id)` - поиск объявлений продавца

**Технологии:** _SQLAlchemy с синхронным движком_

---


### 2. REST Controller

**Эндпоинты:**

| Метод | Path | Описание |
|-------|------|----------|
| POST | `/api/listings` | Создать новое объявление |
| GET | `/api/listings/{listing_id}` | Получить объявление по ID |
| POST | `/api/listings/{listing_id}/approve` | Одобрить объявление |
| POST | `/api/listings/{listing_id}/reject` | Отклонить объявление |
| GET | `/api/listings` | Список активных объявлений с пагинацией |

---


### 3. Docker Compose

**Сервисы:**

- `db` - PostgreSQL 15
- `listing-service` - FastAPI приложение
- `api-gateway` - nginx для маршрутизации

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: listing_db
    environment:
      POSTGRES_DB: listing_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  rabbitmq:
    image: rabbitmq:3-management
    container_name: listing_rabbitmq
    ports:
      - "5672:5672"
      - "15672:15672"
    healthcheck:
      test: ["CMD", "rabbitmqctl", "status"]
      interval: 10s
      timeout: 5s
      retries: 5

  listing-service:
    build: ./services/listing-service
    container_name: listing_service
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/listing_db
      - RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672//
    depends_on:
      db:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    ports:
      - "8000:8000"

  api-gateway:
    image: nginx:alpine
    container_name: api_gateway
    ports:
      - "80:80"
    volumes:
      - ./api_gateway/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - listing-service

volumes:
  postgres_data:
```

---


### 4. Интеграционные тесты

**Тестируемые сценарии:**

- Сохранение объявления через repository → чтение из БД
- Проверка полей: title, price.amount, category.name

**Скриншот pytest:**

_![image.png](image.png)_

---


## Таблица критериев оценки

| Критерий | Баллы | Выполнено |
|----------|-------|-----------|
| Repository: реализация интерфейса, ORM | 25 | ✅ |
| REST Controller: CRUD операции | 25 | ✅ |
| БД: миграции, Docker Compose | 15 | ✅ |
| Event Publisher: публикация событий | 15 | ✅ |
| Интеграционные тесты: SQLite in-memory | 15 | ✅ |
| Качество документации | 5 | ✅ |
| **ИТОГО** | **100** | |

---


## Контрольные вопросы

1. **Почему Repository находится в Infrastructure, а не в Domain?**
   - Repository реализует конкретный механизм доступа к данным (SQLAlchemy, NoSQL, in-memory), что является деталью инфраструктуры. В домене определяется только интерфейс порта (ListingRepository), а его конкретная реализация помещается в инфраструктурный слой, чтобы соблюсти принцип разделения вопросов и позволить заменять механизмы хранения без изменения доменной логики.

2. **В чём преимущество ORM над обычным SQL?**
   - ORM позволяет работать с данными как с объектами домена (Listing, Price, Category), уменьшая количество шаблонного кода для маппинга. Он обеспечивает переносимость между СУБД, поддерживает отложенную загрузку и упрощает управление транзакциями. Для простых CRUD-операций ORM значительно ускоряет разработку.

---


## Ссылка на репозиторий

👉 **GitHub:** _https://github.com/kerubifi_

---


## Вывод

✍️ Реализован инфраструктурный слой системы объявлений «Бери, пока горячее» с использованием SQLAlchemy ORM для маппинга сущности Listing в таблицу listings PostgreSQL. Создан SQLAlchemyListingRepository, который инкапсулирует всю логику сохранения и поиска объявлений в БД. REST-контроллер на FastAPI предоставляет полный набор эндпоинтов для создания, получения, модерации и поиска объявлений. SQLAlchemyListingRepository и ListingORM связывают доменную модель Listing (entity), Price (VO) и Category (VO) с реляционной схемой БД.

---


**Дата выполнения:** _12.05.2026_
**Оценка:** _____________
**Подпись преподавателя:** _____________

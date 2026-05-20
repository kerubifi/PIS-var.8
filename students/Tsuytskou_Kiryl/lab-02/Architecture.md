# Архитектура сервиса объявлений (Listing Service)

Бизнес-логика (Domain) полностью изолирована. 

- **Входящий порт**: `CreateListingUseCase`, `GetListingUseCase`, `ModerateListingUseCase` — определяют, как можно создать, получить и промодерировать объявление.
- **Исходящие порты**: `ListingRepository`, `ModerationService`, `NotificationService` — определяют, что нужно от БД, сервиса модерации и сервиса уведомлений.
- **Адаптеры**: Находятся в слое `infrastructure` и реализуют порты (например, `InMemoryListingRepository`, `MockModerationService`).
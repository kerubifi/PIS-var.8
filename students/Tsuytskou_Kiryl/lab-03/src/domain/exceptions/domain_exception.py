class DomainException(Exception):
    """Базовое исключение для домена"""
    pass


class ListingValidationError(DomainException):
    """Ошибка валидации объявления"""
    pass


class InvalidListingStateError(DomainException):
    """Ошибка некорректного статуса объявления"""
    pass
class DomainException(Exception):
    """Базовое исключение для домена"""
    pass


class ListingValidationError(DomainException):
    """Ошибка валидации объявления"""
    pass


class InvalidListingStateError(DomainException):
    """Ошибка при недопустимой операции с текущим статусом объявления"""
    pass

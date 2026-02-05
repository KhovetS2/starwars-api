"""Domain errors for the application."""


class DomainError(Exception):
    """Base domain error."""

    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class NotFoundError(DomainError):
    """Resource not found error."""

    def __init__(self, resource: str, identifier: str | int):
        super().__init__(f"{resource} with id '{identifier}' not found")
        self.resource = resource
        self.identifier = identifier


class AuthenticationError(DomainError):
    """Authentication failed error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class AuthorizationError(DomainError):
    """Authorization failed error."""

    def __init__(self, message: str = "Not authorized to perform this action"):
        super().__init__(message)


class ValidationError(DomainError):
    """Validation error."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message)


class DuplicateError(DomainError):
    """Duplicate resource error."""

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(f"{resource} with {field} '{value}' already exists")
        self.resource = resource
        self.field = field
        self.value = value

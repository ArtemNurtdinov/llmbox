class ApplicationException(Exception):
    """Base class for application-level errors."""


class ValidationException(ApplicationException):
    """Client error (400): invalid input or unsupported operation."""


class ServiceUnavailableException(ApplicationException):
    """Upstream/service error (502)."""

    def __init__(self, message: str, original_error: Exception | None = None):
        self.original_error = original_error
        super().__init__(message)


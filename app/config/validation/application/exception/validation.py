from app.application.exceptions import ApplicationException


class ConfigurationException(ApplicationException):
    """Startup/configuration error (fail fast on invalid config)."""

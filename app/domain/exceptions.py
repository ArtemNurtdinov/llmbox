class DomainException(Exception):
    pass


class UnknownAIAssistantException(DomainException):
    def __init__(self, assistant: str):
        self.assistant = assistant
        super().__init__(f"Unknown AI assistant: {assistant}")


class AIServiceException(DomainException):
    def __init__(self, message: str, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message)


class InvalidMessageException(DomainException):
    def __init__(self, message: str):
        super().__init__(f"Invalid message: {message}")


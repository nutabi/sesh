class SeshError(Exception):
    """Base class for all Sesh-related errors."""

    def __init__(self, message: str = "Unknown Sesh error occurred.") -> None:
        super().__init__(message)


class NoActiveSeshError(SeshError):
    """Raised when there is no active Sesh session."""

    def __init__(self, message: str = "No active session to stop."):
        super().__init__(message)


class InvalidSeshDataError(SeshError):
    """Raised when there is invalid Sesh data."""

    def __init__(self, message: str = "Invalid Sesh data."):
        super().__init__(message)

class SeshError(Exception):
    """Base class for all Sesh-related errors."""

    def __init__(self, message: str = "Unknown Sesh error occurred.") -> None:
        super().__init__(message)


class NoActiveSeshError(SeshError):
    """Raised when there is no active Sesh."""

    def __init__(self, message: str = "No active Sesh to stop."):
        super().__init__(message)


class InvalidSeshDataError(SeshError):
    """Raised when there is invalid Sesh data."""

    def __init__(self, message: str = "Invalid Sesh data."):
        super().__init__(message)


class SeshInProgressError(SeshError):
    """Raised when there is an ongoing Sesh."""

    def __init__(self, message: str = "A Sesh is already in progress."):
        super().__init__(message)


class MigrationError(SeshError):
    """Raised when a migration fails."""

    def __init__(self, message: str = "Migration failed."):
        super().__init__(message)


class DatabaseError(SeshError):
    """Raised when a database operation fails."""

    def __init__(self, message: str = "Database operation failed."):
        super().__init__(message)


class InvalidTagError(SeshError):
    """Raised when a tag name is invalid."""

    def __init__(self, tag_name: str = "", message: str = ""):
        if not message and tag_name:
            message = f"Invalid tag: {tag_name}"
        elif not message:
            message = "Invalid tag provided."
        super().__init__(message)


class SessionStorageError(SeshError):
    """Raised when session file storage operations fail."""

    def __init__(self, message: str = "Session storage operation failed."):
        super().__init__(message)


class InvalidArgumentError(SeshError):
    """Raised when command arguments are invalid."""

    def __init__(self, message: str = "Invalid command argument."):
        super().__init__(message)

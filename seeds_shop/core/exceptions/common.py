class AppException(Exception):
    """Base Exception"""

    @property
    def message(self) -> str:
        return "An application error occurred"


class ApplicationException(AppException):
    pass


class UnexpectedError(ApplicationException):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass


class RepoError(UnexpectedError):
    pass


class MappingError(ApplicationException):
    pass

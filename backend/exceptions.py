class ShortenerBaseError(Exception):
    pass


class NoDomainFoundError(ShortenerBaseError):
    pass


class DomainAlreadyExistsError(ShortenerBaseError):
    pass


class ExaminationCreateDBError(ShortenerBaseError):
    pass


class DomainValidationError(ShortenerBaseError):
    pass

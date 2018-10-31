"""This module defines custom validation exceptions"""


class ValidationError(Exception):
    """Base class for other exceptions"""
    pass


class InvalidUsernameError(ValidationError):
    """Raised when the username contains non-latin characters"""
    pass


class InvalidEmailError(ValidationError):
    """Raised when the email does not match the template"""
    pass


class InvalidDateError(ValidationError):
    """Raised when the date is not a 'YYYY-MM-DD' string"""
    pass


class NoValueError(ValidationError):
    """Raised when a field is empty"""
    pass

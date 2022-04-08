"""Module containing the exception class for describe-get-system proof of concept module."""


class DGSError(Exception):
    """Use to capture error DGS construction."""


class TemplateStorageError(DGSError):
    """Use to capture error for TemplateStorage."""


class AdaptorAuthenticationError(DGSError):
    """Use to capture error for adaptor connection"""


class InterpreterError(DGSError):
    """Use to capture error for interpreter"""


class NotImplementedFrameworkError(InterpreterError):
    """Use to capture error for not implement framework"""

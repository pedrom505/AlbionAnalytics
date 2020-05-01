import logging


class ApplicationError(Exception):
    """
    Generic exception class used by every exceptions implemented
    """
    def __init__(self, *args):
        self.logger = logging.getLogger(__name__)
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        error_message = self.__class__.__name__
        if self.message:
            error_message += f": {self.message}"

        self.logger.error(error_message)
        return error_message


class InvalidParameter(ApplicationError):
    """
    The InvalidParameter exception is raised when a a invalid parameter is passed to the function
    """


class FileNotFounded(ApplicationError):
    """
    The InvalidParameter exception is raised when a a invalid parameter is passed to the function
    """


class InternalError(ApplicationError):
    """
    The InternalError exception is raised when a operation error occurs in the application
    """


class ConnectionFailure(ApplicationError):
    """
    The ConnectionError exception is raised when a occurs a failure to connect with the specified server
    """
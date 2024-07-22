class BaseScannerException(Exception):
    def __init__(self, error_message: str = None):
        self.error_message = error_message

    def __json__(self):
        return {'error_message': self.error_message}


class JiraError(BaseScannerException):
    ...

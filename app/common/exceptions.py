class InvalidParameterException(Exception):
    def __init__(self, message):
        super(InvalidParameterException, self).__init__(message)


class ResourceExistsException(Exception):
    def __init__(self, message):
        super(ResourceExistsException, self).__init__(message)


class ResourceNotFoundException(Exception):
    def __init__(self, message):
        super(ResourceNotFoundException, self).__init__(message)


class UserNotAuthorizedException(Exception):
    def __init__(self, message):
        super(UserNotAuthorizedException, self).__init__(message)


class CustomException(Exception):
    def __init__(self, message, status_code):
        super(CustomException, self).__init__(message)
        self.status_code = status_code

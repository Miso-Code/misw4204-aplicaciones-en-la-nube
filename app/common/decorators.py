# A decorator that handle exceptions and returns a json response
#
from functools import wraps
from http import HTTPStatus
from models.db import Session

from common.exceptions import ResourceNotFoundException, \
    InvalidParameterException, \
    UserNotAuthorizedException, \
    ResourceExistsException


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        status_code = HTTPStatus.OK
        error = ""
        try:
            return func(*args, **kwargs)
        except ResourceNotFoundException as e:
            status_code = HTTPStatus.NOT_FOUND
            error = str(e)
        except InvalidParameterException as e:
            status_code = HTTPStatus.BAD_REQUEST
            error = str(e)
        except UserNotAuthorizedException as e:
            status_code = HTTPStatus.UNAUTHORIZED
            error = str(e)
        except ResourceExistsException as e:
            status_code = HTTPStatus.CONFLICT
            error = str(e)
        except Exception as e:
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            error = str(e)
        finally:
            if status_code >= HTTPStatus.BAD_REQUEST:
                response_object = {
                    'status': 'error',
                    'message': error,
                }
                return response_object, status_code

    return wrapper


def db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = Session()
        try:
            result = func(session, *args, **kwargs)
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper

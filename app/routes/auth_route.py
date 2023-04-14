from http import HTTPStatus

from flasgger import swag_from
from flask import Blueprint
from flask import request

from services import auth_service

from common.decorators import handle_exceptions

blueprint = Blueprint('auth_api', __name__, url_prefix='/api/auth')


@blueprint.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'User logged in',
        },
    },
})
@handle_exceptions
def login():
    return auth_service.login(request.get_json())


@blueprint.route('/signup', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.CREATED.value: {
            'description': 'User created',
        },
    },
})
@handle_exceptions
def signup():
    return auth_service.signup(request.get_json()), HTTPStatus.CREATED

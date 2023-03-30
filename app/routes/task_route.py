from http import HTTPStatus
from typing import Tuple, Dict, Any

from flasgger import swag_from
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from services import task_service

from common.decorators import handle_exceptions

blueprint = Blueprint('task_api', __name__, url_prefix='/api')


@blueprint.route('/tasks', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Get all user-tasks',
        },
    },
})
@jwt_required()
@handle_exceptions
def get_all_user_tasks() -> Tuple[Dict[str, Any], int]:
    user_id = get_jwt_identity()
    return task_service.get_all_user_tasks(user_id), HTTPStatus.OK

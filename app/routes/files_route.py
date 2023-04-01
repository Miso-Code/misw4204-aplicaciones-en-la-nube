from http import HTTPStatus
from typing import Tuple, Dict, Any

from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services import files_service

from common.decorators import handle_exceptions

blueprint = Blueprint('files_api', __name__, url_prefix='/api')


@blueprint.route('/files', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Obtain specific file by id, and in query param selected to original or converted file',
        },
    },
})
@jwt_required()
@handle_exceptions
def get_file_by_id() -> Tuple[Dict[str, Any], int]:
    file_id = int(request.args.get('id'))
    selected = request.args.get('selected')
    return files_service.get_file_by_id(file_id, selected), HTTPStatus.OK

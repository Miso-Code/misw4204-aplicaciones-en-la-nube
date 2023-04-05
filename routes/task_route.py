from http import HTTPStatus
from typing import Tuple, Dict, Any

from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from celery_jobs import process_file
from common.decorators import handle_exceptions
from services import task_service

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


@blueprint.route('/tasks', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.CREATED.value: {
            'description': 'Create a new task',
        },
    },
})
@jwt_required()
@handle_exceptions
def create_task() -> Tuple[Dict[str, Any], int]:
    user_id = get_jwt_identity()
    task_json = task_service.create_task(user_id, request)
    process_file.delay(task_json)
    return task_json, HTTPStatus.CREATED


@blueprint.route('/tasks/<int:id_task>', methods=['GET'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Get a task by id',
        },
    },
})
@jwt_required()
@handle_exceptions
def get_task_by_id(id_task: int) -> Tuple[Dict[str, Any], int]:
    user_id = get_jwt_identity()
    return task_service.get_task_by_id(user_id, id_task), HTTPStatus.OK


@blueprint.route('/tasks/<int:id_task>', methods=['DELETE'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Delete a task by id',
        },
    },
})
@jwt_required()
@handle_exceptions
def delete_task_by_id(id_task: int) -> Tuple[Dict[str, Any], int]:
    user_id = get_jwt_identity()
    return task_service.delete_task_by_id(user_id, id_task), HTTPStatus.OK

from common.exceptions import CustomException, ResourceNotFoundException
from common.decorators import db_session
from flask import send_from_directory
from models.task import Task
from schemas.task_schema import TaskSchema


@db_session
def get_file_by_id(session, id_task, selected='converted'):
    task = session.query(Task).filter_by(user_id=id_user, id=id_task).first()
    if task is None:
        raise ResourceNotFoundException('Task not found')
    if selected == 'original':
        return send_from_directory('static/files/uploaded', str(task.id) + '.' + task.extension_from,
                                   as_attachment=True)
    elif selected == 'converted':
        return send_from_directory('static/files/converted',
                                   str(task.id) + '.' + task.extension_to, as_attachment=True)
    else:
        raise ResourceNotFoundException('File not found')

from app.common.exceptions import CustomException
from flask import send_from_directory
from models.task import Task
from schemas.task_schema import TaskSchema


def get_file_by_id(id_task, selected='converted'):
    task = Task.query.filter_by(id=id_task).first()
    if task is None:
        raise CustomException('Task not found', 404)
    if selected == 'original':
        return send_from_directory('static/files', str(task.id) + '.' + task.extension_from, as_attachment=True)
    elif selected == 'converted':
        return send_from_directory('static/files/converted',
                                   str(task.id) + '.' + task.extension_to, as_attachment=True)
    else:
        raise CustomException('File not found', 404)

from common.exceptions import CustomException, ResourceNotFoundException
from flask import send_from_directory
from models.task import Task
from schemas.task_schema import TaskSchema


def get_file_by_id(id_task, selected='converted'):
    try:
        task = Task.query.filter_by(id=id_task).first()
        if task is None:
            raise ResourceNotFoundException('Task not found')
        if selected == 'original':
            return send_from_directory('static/files/uploaded', str(task.id) + '.' + task.extension_from, as_attachment=True)
        elif selected == 'converted':
            return send_from_directory('static/files/converted',
                                    str(task.id) + '.' + task.extension_to, as_attachment=True)
        else:
            raise ResourceNotFoundException('File not found')
    except:
        raise CustomException('Error to get file', 500)

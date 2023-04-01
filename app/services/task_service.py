from app.common.exceptions import CustomException
from schemas.task_schema import TaskSchema
import os

from models.task import Task


# get all tasks of the authenticated user
def get_all_user_tasks(id_user):
    task_schema = TaskSchema(many=True)
    return task_schema.dump(Task.query.filter_by(user_id=id_user).all())


def create_task(id_user, request):
    try:
        file = request.files['file']
        extension_to = request.form['new_format']
        extension_from = file.filename.split('.')[-1]
        file.save('static/files/uploaded/' +
                  str(task.id) + '.' + extension_from)
        task = Task(user_id=id_user, file_name=file.filename,
                    extension_from=extension_from, extension_to=extension_to)
        task.save()
        task_schema = TaskSchema()
        return task_schema.dump(task)
    except:
        raise CustomException('Error to create task', 500)


def get_task_by_id(id_user, id_task):
    task = Task.query.filter_by(user_id=id_user, id=id_task).first()
    if task is None:
        raise CustomException('Task not found', 404)
    task_schema = TaskSchema()
    return task_schema.dump(task)


def delete_task_by_id(id_user, id_task):
    task = Task.query.filter_by(user_id=id_user, id=id_task).first()
    if task is None:
        raise CustomException('Task not found', 404)
    task.delete()
    return {'message': 'Task deleted successfully'}

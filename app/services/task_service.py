from common.exceptions import UserNotAuthorizedException
from common.exceptions import CustomException
from schemas.task_schema import TaskSchema
from common.utils import save_changes
import os

from models.task import Task


# get all tasks of the authenticated user
def get_all_user_tasks(id_user):
    try:
        task_schema = TaskSchema(many=True)
        return task_schema.dump(Task.query.filter_by(user_id=id_user).all())
    except:
        raise UserNotAuthorizedException()


def create_task(id_user, request):
    try:
        file = request.files['file']
        extension_to = request.form['new_format']
        extension_from = file.filename.split('.')[-1]
        file_name= file.filename.split('.')[0]
        task = Task(user_id=id_user, file_name=file_name,
                    extension_from=extension_from, extension_to=extension_to)
        save_changes(task)
        file.save('static/files/uploaded/' +
                  str(task.id) + '.' + extension_from)
        task_schema = TaskSchema()
        return task_schema.dump(task)
    except Exception as e:
        raise CustomException('Error to create task '+ str(e), 500)


def get_task_by_id(id_user, id_task):
    try:
        task = Task.query.filter_by(user_id=id_user, id=id_task).first()
        if task is None:
            raise CustomException('Task not found', 404)
        task_schema = TaskSchema()
        return task_schema.dump(task)
    except:
        raise UserNotAuthorizedException()


def delete_task_by_id(id_user, id_task):
    try:
        task = Task.query.filter_by(user_id=id_user, id=id_task).first()
        if task is None:
            raise CustomException('Task not found', 404)
        task.delete()
        return {'message': 'Task deleted successfully'}
    except:
        raise UserNotAuthorizedException()

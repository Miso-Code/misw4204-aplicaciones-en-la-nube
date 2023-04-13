import os
from common.exceptions import CustomException
from common.exceptions import UserNotAuthorizedException
from common.utils import delete_changes, save_changes
from models.task import Task
from schemas.task_schema import TaskSchema


# get all tasks of the authenticated user
def get_all_user_tasks(id_user):
    try:
        task_schema = TaskSchema(many=True)
        return task_schema.dump(Task.query.filter_by(user_id=id_user).all())
    except:
        raise UserNotAuthorizedException()


def create_task(id_user, request):
    valid_formats = ['zip', '7z', 'tar.gz', 'tar.bz2']
    try:
        file = request.files.get('file')
        extension_to = request.form.get('new_format')
        
        extension_from = file.filename.split('.')[-1]
        file_name = file.filename.split('.')[0]

        if not all([file, extension_to, extension_from, file_name]):
            raise CustomException('All fields are required.', 400)
        if extension_to.lower() not in valid_formats:
            raise CustomException('Unsupported output format', 400)
        if extension_from.lower() not in valid_formats:
            raise CustomException('Unsupported input format', 400)
        if extension_from.lower() == extension_to.lower():
            raise CustomException('Input and output formats are the same', 400)

        task = Task(user_id=id_user,
                    file_name=file_name,
                    extension_from=extension_from,
                    extension_to=extension_to)

        save_changes(task)
        file.save(f'static/files/uploaded/{task.id}.{extension_from}')
        task_schema = TaskSchema()
        return task_schema.dump(task)
    except Exception as e:
        if isinstance(e, CustomException):
            raise e
        raise CustomException('Error to create task ' + str(e), 500)


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
        os.remove(f'./static/files/uploaded/{task.id}.{task.extension_from}')
        os.remove(f'./static/files/converted/{task.id}.{task.extension_to}')
        
        delete_changes(task)
        return {'message': 'Task deleted successfully'}
    except Exception as e:
        raise CustomException('Error to delete task ' + str(e), 500)


def update_task_status(id_task, status):
    try:
        task = Task.query.filter_by(id=id_task).first()
        if task is None:
            raise CustomException('Task not found', 404)
        task.status = status
        save_changes(task)
    except:
        raise UserNotAuthorizedException()

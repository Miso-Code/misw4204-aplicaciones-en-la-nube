import os
from common.exceptions import CustomException
from common.exceptions import UserNotAuthorizedException
from common.utils import delete_changes, save_changes
from common.decorators import db_session
from models.task import Task
from schemas.task_schema import TaskSchema

task_schema = TaskSchema()


# get all tasks of the authenticated user
@db_session
def get_all_user_tasks(session, id_user):
    tasks = session.query(Task).filter_by(user_id=id_user).all()
    return task_schema.dump(tasks, many=True)


@db_session
def create_task(session, id_user, request):
    valid_formats = ['zip', '7z', 'tar.gz', 'tar.bz2']
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
    save_changes(session, task)
    file.save(f'static/files/uploaded/{task.id}.{extension_from}')
    return task_schema.dump(task)


@db_session
def get_task_by_id(session, id_user, id_task):
    task = session.query(Task).filter_by(user_id=id_user, id=id_task).first()
    if task is None:
        raise CustomException('Task not found', 404)
    return task_schema.dump(task)


@db_session
def delete_task_by_id(session, id_user, id_task):
    task = session.query(Task).filter_by(user_id=id_user, id=id_task).first()
    if task is None:
        raise CustomException('Task not found', 404)
    os.remove(f'./static/files/uploaded/{task.id}.{task.extension_from}')
    os.remove(f'./static/files/converted/{task.id}.{task.extension_to}')
    session.delete(task)
    return {'message': 'Task deleted successfully'}


@db_session
def update_task_status(session, id_task, status):
    task = session.query(Task).filter_by(id=id_task).first()
    if task is None:
        raise CustomException('Task not found', 404)
    task.status = status
    save_changes(session, task)
    return task_schema.dump(task)

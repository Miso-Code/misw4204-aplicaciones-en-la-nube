from common.exceptions import CustomException, ResourceNotFoundException
from common.decorators import db_session
from common.cloud_storage_wrapper import CloudStorageWrapper
from flask import send_from_directory
from models.task import Task
from schemas.task_schema import TaskSchema


@db_session
def get_file_by_id(session, id_task, selected='converted'):
    task = session.query(Task).filter_by(user_id=id_user, id=id_task).first()
    cs_wrapper = CloudStorageWrapper()
    if task is None:
        raise ResourceNotFoundException('Task not found')
    if selected == 'original':
        # get file from bucket
        file = cs_wrapper.get_file('files/uploaded/' + str(task.id) + '.' + task.extension_from)
        return file
    elif selected == 'converted':
        file = cs_wrapper.get_file('files/converted/' + str(task.id) + '.' + task.extension_to)
        return file
    else:
        raise ResourceNotFoundException('File not found')

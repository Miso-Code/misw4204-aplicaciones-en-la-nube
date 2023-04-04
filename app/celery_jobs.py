import os
import tarfile
import zipfile

import pylzma
from celery import Celery

from models.status import Status
from services.task_service import update_task_status

celery = Celery(__name__)

# Set up configuration settings
celery.conf.update(
    broker_url= os.environ.get('REDIS_URL'),
    result_backend= os.environ.get('REDIS_URL'),
    task_track_started=True,
)


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)


@celery.task(bind=True)
def process_file(job, task):
    extension_to = task['extension_to']
    extension_from = task['extension_from']

    file_name = task['id']

    files_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/static/files'

    input_file_path = files_path + f'/uploaded/{file_name}.{extension_from}'
    output_file_path = files_path + f'/converted/{file_name}.{extension_to}'

    if extension_to == 'zip':
        zip_file = zipfile.ZipFile(output_file_path, 'w')
        zip_file.write(input_file_path, arcname=os.path.basename(input_file_path))
        zip_file.close()

    elif extension_to == '7z':
        file_content = read_file(input_file_path)
        compressed_contents = pylzma.compress(file_content)
        file_content = compressed_contents
        write_file(output_file_path, file_content)

    elif extension_to == 'tar.gz':
        with tarfile.open(output_file_path, 'w:gz') as tar_file:
            tar_file.add(input_file_path, arcname=os.path.basename(input_file_path))

    elif extension_to == 'tar.bz2':
        with tarfile.open(output_file_path, 'w:bz2') as tar_file:
            tar_file.add(input_file_path, arcname=os.path.basename(input_file_path))

    update_task_status(task['id'], Status.PROCESSED.value)

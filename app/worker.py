import json
import os
import tarfile
import zipfile
import io
from concurrent.futures import TimeoutError
import base64
import tempfile
from pathlib import Path

import pylzma
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber import exceptions as sub_exceptions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, request

from common.connections import get_cloudsql_connection
from common.cloud_storage_wrapper import CloudStorageWrapper
from models.status import Status
from models.task import Task  # noqa
from models.user import User  # noqa

project_id = os.getenv("PROJECT_ID")
subscription_id = os.getenv("SUBSCRIPTION_ID")

app = Flask(__name__)


@app.route("/", methods=["POST"])
def pub_sub_subscriber():
    envelope = json.loads(request.data.decode('utf-8'))
    payload = base64.b64decode(envelope['message']['data'])
    task = json.loads(payload.decode('utf-8'))
    convert_file(task)
    return 'Task converted', 200


def convert_file(task):
    cs_wrapper = CloudStorageWrapper()

    extension_to = task['extension_to'].lower()
    extension_from = task['extension_from'].lower()

    file_name = task['id']

    input_file = cs_wrapper.get_file(f'files/uploaded/{file_name}.{extension_from}')
    output_file = io.BytesIO()  # Create a temporary file in memory
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file_path = Path(temp_file.name)
        temp_file.write(input_file)

        if extension_to == 'zip':
            with zipfile.ZipFile(output_file, 'w') as zip_file:
                zip_file.write(temp_file_path, arcname=f'{file_name}.{extension_from}')

        elif extension_to == '7z':
            compressed_contents = pylzma.compress(temp_file_path.read_bytes())
            output_file.write(compressed_contents)

        elif extension_to == 'tar.gz':
            with tarfile.open(fileobj=output_file, mode='w:gz') as tar_file:
                tar_file.add(temp_file_path, arcname=f'{file_name}.{extension_from}')

        elif extension_to == 'tar.bz2':
            with tarfile.open(fileobj=output_file, mode='w:bz2') as tar_file:
                tar_file.add(temp_file_path, arcname=f'{file_name}.{extension_from}')

    output_file.seek(0)  # Reset the file position to the beginning
    cs_wrapper.upload_file(f'files/converted/{file_name}.{extension_to}', output_file.getvalue())
    update_task_status(task['id'], Status.PROCESSED.value)


def get_file(bytes_io):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(bytes_io.getvalue())
    return Path(temp_file.name)


def db_wrapper():
    engine = create_engine(
        "postgresql+pg8000://",
        creator=get_cloudsql_connection,
    )
    db = declarative_base()
    db.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def update_task_status(task_id, status):
    session = db_wrapper()
    task = session.query(Task).filter(Task.id == task_id).first()
    task.status = status
    session.commit()
    session.close()


def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

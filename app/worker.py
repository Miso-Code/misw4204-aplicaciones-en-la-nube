import json
import os
import tarfile
import zipfile
from concurrent.futures import TimeoutError

import pylzma
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber import exceptions as sub_exceptions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.cloud_storage_wrapper import CloudStorageWrapper
from models.status import Status
from models.task import Task  # noqa
from models.user import User  # noqa

project_id = os.getenv("PROJECT_ID")
subscription_id = os.getenv("SUBSCRIPTION_ID")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    ack_future = message.ack_with_response()

    try:
        ack_future.result()
        print(f"Ack for message {message.message_id} successful.")
    except sub_exceptions.AcknowledgeError as e:
        print(
            f"Ack for message {message.message_id} failed with error: {e.error_code}"
        )

    task = json.loads(message.data.decode("utf-8"))

    cs_wrapper = CloudStorageWrapper()

    extension_to = task['extension_to'].lower()
    extension_from = task['extension_from'].lower()

    file_name = task['id']

    files_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/static/files'

    input_file_path = files_path + f'/uploaded/{file_name}.{extension_from}'
    output_file_path = files_path + f'/converted/{file_name}.{extension_to}'

    cs_wrapper.get_file_into_filename(f'files/uploaded/{file_name}.{extension_from}', input_file_path)

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
    cs_wrapper.upload_file_from_path(f'/converted/{file_name}.{extension_to}', output_file_path)
    # remove local files
    os.remove(output_file_path)
    os.remove(input_file_path)
    update_task_status_wrapper(task['id'], Status.PROCESSED.value)


def run_worker():
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result()
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


def db_wrapper():
    db_uri = os.environ.get('DB_URI')
    engine = create_engine(db_uri)
    db = declarative_base()
    db.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


def update_task_status_wrapper(task_id, status):
    session = db_wrapper()
    task = session.query(Task).filter(Task.id == task_id).first()
    task.status = status
    session.commit()
    session.close()


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)


run_worker()

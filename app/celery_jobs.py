##########################################################
#### DEPRECATED IN FAVOR OF USING OFFICIAL PUBSUB SDK ####
##########################################################

# import os
# import tarfile
# import zipfile
# import os
# import pylzma
# from celery import Celery
# from common.cloud_storage_wrapper import CloudStorageWrapper
#
# from models.status import Status
#
# from models.user import User  # noqa
# from models.task import Task  # noqa
#
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
#
# app = Celery('tasks', broker=os.environ.get('BROKER_URL', 'redis://localhost:6379/0'))
#
#
# def db_wrapper():
#     db_uri = os.environ.get('DB_URI')
#     engine = create_engine(db_uri)
#     db = declarative_base()
#     db.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#     return Session()
#
#
# def update_task_status_wrapper(task_id, status):
#     session = db_wrapper()
#     task = session.query(Task).filter(Task.id == task_id).first()
#     task.status = status
#     session.commit()
#     session.close()
#
#
# def read_file(file_path):
#     with open(file_path, 'rb') as file:
#         return file.read()
#
#
# def write_file(file_path, data):
#     with open(file_path, 'wb') as file:
#         file.write(data)
#
#
# @app.task(bind=True)
# def process_file(job, task):
#     cs_wrapper = CloudStorageWrapper()
#
#     extension_to = task['extension_to'].lower()
#     extension_from = task['extension_from'].lower()
#
#     file_name = task['id']
#
#     files_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/static/files'
#
#     input_file_path = files_path + f'/uploaded/{file_name}.{extension_from}'
#     output_file_path = files_path + f'/converted/{file_name}.{extension_to}'
#
#     cs_wrapper.get_file_into_filename(f'files/uploaded/{file_name}.{extension_from}', input_file_path)
#
#     if extension_to == 'zip':
#         zip_file = zipfile.ZipFile(output_file_path, 'w')
#         zip_file.write(input_file_path, arcname=os.path.basename(input_file_path))
#         zip_file.close()
#
#     elif extension_to == '7z':
#         file_content = read_file(input_file_path)
#         compressed_contents = pylzma.compress(file_content)
#         file_content = compressed_contents
#         write_file(output_file_path, file_content)
#
#     elif extension_to == 'tar.gz':
#         with tarfile.open(output_file_path, 'w:gz') as tar_file:
#             tar_file.add(input_file_path, arcname=os.path.basename(input_file_path))
#
#     elif extension_to == 'tar.bz2':
#         with tarfile.open(output_file_path, 'w:bz2') as tar_file:
#             tar_file.add(input_file_path, arcname=os.path.basename(input_file_path))
#     cs_wrapper.upload_file_from_path(f'/converted/{file_name}.{extension_to}', output_file_path)
#     # remove local files
#     os.remove(output_file_path)
#     os.remove(input_file_path)
#     update_task_status_wrapper(task['id'], Status.PROCESSED.value)

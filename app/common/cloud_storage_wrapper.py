from google.cloud import storage
import io


class CloudStorageWrapper:
    client = storage.Client()
    bucket_name = 'misw4204-aplicaciones-en-la-nube'

    def __init__(self):
        self.bucket = self.client.get_bucket(self.bucket_name)

    # Get file as bytes from bucket
    def get_file(self, file_name):
        blob = self.bucket.blob(file_name)
        return blob.download_as_bytes()

    # Download a file into local filename
    def get_file_into_filename(self, file_name, output_filename):
        blob = self.bucket.blob(file_name)
        return blob.download_to_filename(output_filename)

    # Upload a bytes-like file to bucket
    def upload_file(self, file_name, file):
        blob = self.bucket.blob(file_name)
        if not isinstance(file, bytes):
            file.seek(0)
            file_content = file.read()
        else:
            file_content = file
        bytes_file = io.BytesIO(file_content)
        if hasattr(file, 'content_type'):
            blob.upload_from_file(bytes_file, content_type=file.content_type)
        else:
            blob.upload_from_file(bytes_file, content_type='application/octet-stream')

    # Upload a file from path to bucket
    def upload_file_from_path(self, file_name, source_file_name):
        blob = self.bucket.blob(file_name)
        blob.upload_from_filename(filename=source_file_name)

    # Delete file from bucket
    def delete_file(self, file_name):
        blob = self.bucket.blob(file_name)
        blob.delete()

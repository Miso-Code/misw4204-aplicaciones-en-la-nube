import json

from google.cloud import secretmanager


class SecretManagerWrapper:

    def __init__(self, project_id, secret_name, secret_version='latest'):
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = project_id
        self.secret_name = secret_name
        self.secret_version = secret_version

    def get_secret_value(self):
        name = f'projects/{self.project_id}/secrets/{self.secret_name}/versions/{self.secret_version}'
        response = self.client.access_secret_version(request={'name': name})
        return json.loads(response.payload.data.decode('UTF-8'))

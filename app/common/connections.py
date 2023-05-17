import os

from common.secret_manager import SecretManagerWrapper
from google.cloud.sql.connector import Connector, IPTypes

PROJECT_ID = os.getenv('PROJECT_ID')

credentials = SecretManagerWrapper(PROJECT_ID, 'DB_CREDENTIALS')

connection_name = f'{credentials["PROJECT_ID"]}:{credentials["REGION"]}:{credentials["INSTANCE_NAME"]}'


def get_cloudsql_connection():
    with Connector() as connector:
        conn = connector.connect(
            connection_name,
            "pg8000",
            user=credentials["DB_USERNAME"],
            password=credentials["DB_PASSWORD"],
            db=credentials["DB_NAME"],
            ip_type=IPTypes.PRIVATE
        )
        return conn

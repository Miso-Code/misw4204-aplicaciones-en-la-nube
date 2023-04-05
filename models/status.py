from enum import Enum


class Status(str, Enum):
    UPLOADED = 'UPLOADED'
    PROCESSED = 'PROCESSED'

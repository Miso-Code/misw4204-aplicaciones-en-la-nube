import datetime

from sqlalchemy import Enum as SqlEnum

from .db import db
from .status import Status
from sqlalchemy import Column
from sqlalchemy import event
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime


class Task(db):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    extension_from = Column(String(7))
    extension_to = Column(String(7))
    file_name = Column(String(50))
    timestamp = Column(DateTime(), default=datetime.datetime.now())
    status = Column(SqlEnum(Status), default=Status.UPLOADED)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

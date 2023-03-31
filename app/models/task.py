from sqlalchemy import Enum as SqlEnum

from .db import db
from .status import Status


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    extension_from = db.Column(db.String(5))
    extension_to = db.Column(db.String(5))
    file_name = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime(), default=db.func.now())
    status = db.Column(SqlEnum(Status), default=Status.UPLOADED.value)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

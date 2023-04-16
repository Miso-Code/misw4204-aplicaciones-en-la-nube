from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models.task import Task


class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True

    id = fields.Integer()
    extension_from = fields.String()
    extension_to = fields.String()
    file_name = fields.String()
    timestamp = fields.String()
    status = fields.String()

from schemas.task_schema import TaskSchema

from models.task import Task


# get all tasks of the authenticated user
def get_all_user_tasks(id_user):
    task_schema = TaskSchema(many=True)
    return task_schema.dump(Task.query.filter_by(user_id=id_user).all())

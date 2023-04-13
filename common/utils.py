from typing import Any

from models.db import db


def save_changes(data: Any) -> None:
    db.session.add(data)
    db.session.commit()

def delete_changes(data: Any) -> None:
    db.session.delete(data)
    db.session.commit()

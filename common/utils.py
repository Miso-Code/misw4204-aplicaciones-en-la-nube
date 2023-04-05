from typing import Any

from models.db import db


def save_changes(data: Any) -> None:
    db.session.add(data)
    db.session.commit()

from typing import Any

from models.db import db


def save_changes(session, data: Any) -> None:
    session.add(data)
    session.commit()


def delete_changes(session, data: Any) -> None:
    session.delete(data)
    session.commit()

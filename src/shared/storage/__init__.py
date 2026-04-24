from .database import Database
from shared.models.base import BaseModel


def get_db() -> Database:
    db = Database()
    db.init_db(BaseModel)
    return db
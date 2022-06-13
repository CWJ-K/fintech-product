from src.backend.db.router import Router
from src.backend.db.db import *

router = Router()


def get_db_router():
    return router
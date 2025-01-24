from sqlalchemy import select, insert, update

from . import db
from .models import *


def add_data():
    with db.engine.connect() as conn:
        result = conn.execute(select(Initialised)).first()

        if result is None:
            print("Need to add data", flush=True)
        else:
            print("Data Present", flush=True)

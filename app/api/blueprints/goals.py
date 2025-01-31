from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

goals_blueprint = Blueprint("goals", __name__, url_prefix="/goals")


@goals_blueprint.route("/", methods=["GET"])
def goals_handler():
    if request.method == "GET":
        return get_goals_handler()
    return jsonify({"endpoint": "GET_goals_handler"}), 500

def get_goals_handler():

    statement = select(EnergySavingGoals)

    with db.engine.connect() as conn:
        results = conn.execute(statement)

    data_to_send = []
    for result in results:
        (
            goalId,
            name,
            target,
            progress,
            complete,
            date,
        ) = result

        # Data processing here

        entry = {
            "goalId": goalId,
            "name": name,
            "target": target,
            "progress": progress,
            "complete": complete,
            "date": date,
        }
        data_to_send.append(entry)

    return jsonify(data_to_send), 200
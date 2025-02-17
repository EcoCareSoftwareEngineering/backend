from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete
from jsonschema import *

from ...models import *
from ... import db

goals_blueprint = Blueprint("goals", __name__, url_prefix="/goals")

# GET - get all goals


@goals_blueprint.route("/", methods=["GET", "POST"])
def goals_handler():
    if request.method == "GET":
        return get_goals_handler()
    elif request.method == "POST":
        return post_goal_handler()
    return jsonify({"endpoint": "GET_goals_handler"}), 500


def get_goals_handler():
    if request.args.get("complete") == "true":
        statement = select(EnergySavingGoals).where(
            EnergySavingGoals.complete == "true"
        )
    elif request.args.get("complete") == "false":
        statement = select(EnergySavingGoals).where(
            EnergySavingGoals.complete == "false"
        )
    else:
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

    # POST - create a new goal


def post_goal_handler():
    # Validate
    jsonresult = request.json
    if jsonresult is None:
        return "", 500
    else:
        try:
            validate(
                jsonresult,
                {
                    "id": "auto",
                    "title": "Energy Goal",
                    "description": "an energy saving goal",
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "target": {"type": "integer"},
                        "date": {"type": "string"},
                    },
                    "required": ["target"],
                },
            )
        except:
            return "", 500  # return error if validation can't be confirmed

    new_goal = (
        insert(EnergySavingGoals)
        .values(
            name=jsonresult["name"],
            target=jsonresult["target"],
            date=jsonresult["date"],
        )
        .returning(EnergySavingGoals.goalId)
    )

    with db.engine.connect() as conn:
        newId = conn.execute(new_goal).first()
        conn.commit()

    if newId is None:
        return "", 500

    result = select(EnergySavingGoals).where(EnergySavingGoals.goalId == newId[0])

    if result is None:
        return "", 500

    (
        goalId,
        name,
        target,
        progress,
        complete,
        date,
    ) = result

    entry = {
        "goalId": goalId,
        "name": name,
        "target": target,
        "progress": progress,
        "complete": complete,
        "date": date,
    }

    return jsonify(entry), 200


@goals_blueprint.route("/<int:goalId>/", methods=["PUT", "DELETE"])
def goals_update_handler(goal_id: int):
    if request.method == "PUT":
        return put_goal_update_handler(goal_id)
    elif request.method == "DELETE":
        return delete_goal_handler(goal_id)
    return jsonify({"Error": "Invalid"}), 500


# PUT - update a goal
def put_goal_update_handler(goal_id: int):
    jsonresult = request.json
    jlength = len(jsonresult)
    if jlength < 4 and jlength > 0:

        try:
            validate(
                jsonresult,
                {
                    "id": "auto",
                    "title": "Energy Goal",
                    "description": "an energy saving goal",
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "target": {"type": "integer"},
                        "date": {"type": "string"},
                    },
                },
            )
        except:
            return "", 500  # return error if validation can't be confirmed

    if jlength == 1:
        if "name" in jsonresult:
            statement = (
                update(EnergySavingGoals)
                .where(EnergySavingGoals.goalId == goal_id)
                .values(date=jsonresult["name"])
            )
        elif "date" in jsonresult:
            statement = (
                update(EnergySavingGoals)
                .where(EnergySavingGoals.goalId == goal_id)
                .values(date=jsonresult["date"])
            )
        elif "target" in jsonresult:
            statement = (
                update(EnergySavingGoals)
                .where(EnergySavingGoals.goalId == goal_id)
                .values(target=jsonresult["target"])
            )
    elif jlength == 2:
        if "name" and "date" in jsonresult:
            statement = (
                update(EnergySavingGoals)
                .where(EnergySavingGoals.goalId == goal_id)
                .values(date=jsonresult["date"], name=jsonresult["name"])
            )
        elif "name" and "target" in jsonresult:
            statement = (
                update(EnergySavingGoals)
                .where(EnergySavingGoals.goalId == goal_id)
                .values(target=jsonresult["target"], name=jsonresult["name"])
            )
        elif "target" and "date" in jsonresult:
            statement = (
                update(EnergySavingGoals)
                .where(EnergySavingGoals.goalId == goal_id)
                .values(date=jsonresult["date"], target=jsonresult["target"])
            )
    elif jlength == 3:
        statement = (
            update(EnergySavingGoals)
            .where(EnergySavingGoals.goalId == goal_id)
            .values(
                target=jsonresult["target"],
                target=jsonresult["target"],
                date=jsonresult["date"],
            )
        )
    elif jlength > 4:
        return (
            "",
            500,
        )
    statement = select(EnergySavingGoals).where(EnergySavingGoals.goalId == goal_id)

    with db.engine.connect() as conn:
        result = conn.execute(statement).first()
    if result is None:
        return "", 500
    (
        goalId,
        name,
        target,
        progress,
        complete,
        date,
    ) = result

    entry = {
        "goalId": goalId,
        "name": name,
        "target": target,
        "progress": progress,
        "complete": complete,
        "date": date,
    }

    return jsonify(entry), 200


# delete - delete a goal
def delete_goal_handler(goal_id: int):
    statement = delete(EnergySavingGoals).where(EnergySavingGoals.goalId == goal_id)
    with db.engine.connect() as conn:
        conn.execute(statement)
        conn.commit()

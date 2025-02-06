from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

goals_blueprint = Blueprint("goals", __name__, url_prefix="/goals")

# GET - get all goals

@goals_blueprint.route("/", methods=["GET"])
def goals_handler():
    if request.method == "GET":
        return get_goals_handler()
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
    data = request.get_json()

    # Validate
    if not data or "name" not in data or "target" not in data or "date" not in data :
        return jsonify({"Error": "Missing required fields: name, target or date"}), 400

    # Create and save new tag
    new_goal = EnergySavingGoals(name=data["name"],target=data["target"],date=data["date"] )

    try:
        db.session.add(new_goal)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Goal created successfully",
                    "tagId": new_goal.goalId,
                    "name": new_goal.name,
                    "target": new_goal.target,
                    "progress": new_goal.progress,
                    "complete": new_goal.complete,
                    "date": new_goal.date,
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()  
        return (
            jsonify({"Error": f"Couldn't create goal: {str(e)}"}),
            500,
        )

from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete

from ...models import *
from ... import db

goals_blueprint = Blueprint("goals", __name__, url_prefix="/goals")

# GET - get all goals

@goals_blueprint.route("/", methods=["GET","POST"])
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
    data = request.get_json()

    # Validate
    if not data or "name" not in data or "target" not in data or "date" not in data :
        return jsonify({"Error": "Missing required fields: name, target or date"}), 400

    new_goal = EnergySavingGoals(name=data["name"],target=data["target"],date=data["date"] )

    try:
        with db.engine.connect() as conn:
             result = conn.execute(
                 insert(EnergySavingGoals).values(new_goal))
             conn.commit()

    
    except Exception as e:
        db.session.rollback()  
        return (
            jsonify({"Error": f"Couldn't create goal: {str(e)}"}),
            500,  
        )
 
    @goals_blueprint.route("/<int:goalId>/", methods=["PUT", "DELETE"])
    def automations_update_handler(goal_id: int):
        if request.method == "PUT":
            return put_goal_update_handler(goalId)
        elif request.method == "DELETE":
            return delete_goal_update_handler(goalId)
        return jsonify({"Error": "Invalid"}), 500

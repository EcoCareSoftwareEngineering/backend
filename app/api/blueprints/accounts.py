from flask import Blueprint, jsonify, request
from jsonschema import validate
from sqlalchemy import select, insert
import hashlib
import secrets


from ...models import *
from ... import db, tokens

accounts_blueprint = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts_blueprint.route("/login/", methods=["POST"])
def login_handler():
    json = request.json

    if json is None:
        return "", 500

    try:
        validate(
            json,
            {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                },
                "required": ["username", "password"],
            },
        )
    except:
        return "", 500

    statement = select(Users).where(Users.username == json["username"])
    with db.engine.connect() as conn:
        result = conn.execute(statement).first()

    if result is None:
        return "", 500

    _, _, passwordHash, salt = result

    hash = hashlib.sha256((json["password"] + salt).encode())

    if hash.hexdigest() == passwordHash:
        token = secrets.token_urlsafe()
        if json["username"] == "touchscreen":
            tokens["local"] = token
        else:
            tokens["remote"].append(token)
        return jsonify({"token": token}), 200
    else:
        return jsonify(), 500


@accounts_blueprint.route("/signup/", methods=["POST"])
def signup_handler():
    json = request.json
    if json is None:
        return "", 500

    try:
        validate(
            json,
            {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "password": {"type": "string"},
                },
                "required": ["username", "password"],
            },
        )
    except:
        return "", 500

    statement = select(Users).where(Users.username == json["username"])
    with db.engine.connect() as conn:
        result = conn.execute(statement).first()

    if result is not None:
        return "", 500

    salt = secrets.token_hex(16)
    hash = hashlib.sha256((json["password"] + salt).encode())

    statement = insert(Users).values(
        username=json["username"], passwordHash=hash.hexdigest(), salt=salt
    )
    with db.engine.connect() as conn:
        conn.execute(statement)
        conn.commit()

    return "", 200

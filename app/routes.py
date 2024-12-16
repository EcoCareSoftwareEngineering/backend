from flask import Blueprint

main = Blueprint("main", __name__, url_prefix="/api")


@main.route("/")
def index():
    return {"Data": "Results"}

from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete
from ...models import *
from ... import db
from ...routes import check_authentication

# Create a blueprint for the "tags" route, which prefix will be "api/tags"
tags_blueprint = Blueprint("tags", __name__, url_prefix="/tags")


# DEfine the route for GET and POST
@tags_blueprint.route("/", methods=["GET", "POST"])
@check_authentication
def tags_handler():
    if request.method == "GET":
        return get_tags_handler()
    elif request.method == "POST":
        return post_tags_handler()
    return jsonify({"Error": "Invalid"}), 500


# GET - retrieve tags from the db
def get_tags_handler():
    # GET /tags?tagType=category
    tag_type = request.args.get("tagType")

    # If tagType is provided, validate it
    if tag_type:
        try:
            # Convert tagType to Enum
            tag_type = TagType[tag_type.capitalize()]
        except KeyError:
            return jsonify({"Error": "Invalid tagType value"}), 400
        statement = select(Tags).where(Tags.tagType == tag_type)
    else:
        statement = select(Tags)  # Fetch all tags if no filter is applied

    try:
        with db.engine.connect() as conn:
            results = conn.execute(statement).fetchall()

        response = [
            {"tagId": tag.tagId, "name": tag.name, "tagType": tag.tagType.name}
            for tag in results
        ]
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": f"An error occured while fetching tag: {str(e)}"}), 500


# POST - create a new tag
def post_tags_handler():
    # Get data from request
    data = request.get_json()

    # Validate input fields
    if not data or "name" not in data or "tagType" not in data:
        return jsonify({"Error": "Missing required fields: name, tagType"}), 400

    try:
        # Convert tagType to Enum
        tag_type = TagType[data["tagType"].capitalize()]
    except KeyError:
        return jsonify({"Error": "Invalid tagType value"}), 400

    # Prepares sql insert statement to add tags
    statement = insert(Tags).values(name=data["name"], tagType=tag_type)
    try:
        with db.engine.connect() as conn:
            result = conn.execute(statement)
            conn.commit()

            # Fetch the inserted tag
            tag_id = (
                result.inserted_primary_key[0] if result.inserted_primary_key else None
            )
        return jsonify({"message": "Tag created successfully", "tagId": tag_id}), 201

    except Exception as e:
        return (
            jsonify({"Error": f"An error occurred while creating the tag: {str(e)}"}),
            500,
        )


# route supports GET & DELETE for tag_id
@tags_blueprint.route("/<int:tag_id>", methods=["GET", "DELETE"])
@check_authentication
def tag_handle(tag_id):
    if request.method == "GET":
        return get_single_tag(tag_id)
    elif request.method == "DELETE":
        return delete_tag_handler(tag_id)


# GET single tag
def get_single_tag(tag_id):
    statement = select(Tags).where(Tags.tagId == tag_id)

    try:
        with db.engine.connect() as conn:
            result = conn.execute(statement).fetchone()
            if result is None:
                return jsonify({"Error": f"Tag with id {tag_id} not found"}), 404

            return (
                jsonify(
                    {
                        "tagId": result.tagId,
                        "name": result.name,
                        "tagType": result.tagType.name,
                    }
                ),
                200,
            )
    except Exception as e:
        return jsonify({"Error": f"An error occured while fetching tag: {str(e)}"}), 500


# DELETE - delete tag
def delete_tag_handler(tag_id):
    statement = select(Tags).where(Tags.tagId == tag_id)

    try:
        with db.engine.connect() as conn:
            result = conn.execute(statement).fetchone()
            if result is None:
                return jsonify({"Error": f"Tag with id {tag_id} not found"}), 404

            delete_statement = delete(Tags).where(Tags.tagId == tag_id)
            conn.execute(delete_statement)
            conn.commit()

        return jsonify({"message": f"Tag with id: {tag_id} deleted succesfuly"}), 200
    except Exception as e:
        return (
            jsonify({"Error": f"An error occured while deleting the tag: {str(e)}"}),
            500,
        )

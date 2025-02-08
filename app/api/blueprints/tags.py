from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert, update, delete
from ...models import *
from ... import db

# Create a blueprint for the "tags" route, which prefix will be "api/tags"
tags_blueprint = Blueprint("tags", __name__, url_prefix="/tags")


# DEfine the route for GET and POST
@tags_blueprint.route("/", methods=["GET", "POST"])
def tags_handler():
    if request.method == "GET":
        return get_tags_handler()
    elif request.method == "POST":
        return post_tags_handler()
    return jsonify({"Error": "Invalid"}), 500


# GET - retrieve tags from the db
def get_tags_handler():
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

    with db.engine.connect() as conn:
        results = conn.execute(statement)

    response = [
        {"tagId": tag.tagId, "name": tag.name, "tagType": tag.tagType.name}
        for tag in results
    ]
    return jsonify(response), 200


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

    # Create and save new tag
    new_tag = Tags(name=data["name"], tagType=tag_type)

    try:
        db.session.add(new_tag)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Tag created successfully",
                    "tagId": new_tag.tagId,
                    "name": new_tag.name,
                    "tagType": new_tag.tagType.name,
                }
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()  # Rollback in case of any errors
        return (
            jsonify({"Error": f"An error occurred while creating the tag: {str(e)}"}),
            500,
        )

# route supports GET & DELETE for tag_id
@tags_blueprint.route("/<int:tag_id>", methods=["GET", "DELETE"])
def tag_handle(tag_id):
    if request.method == "GET":
        return get_single_tag(tag_id)
    elif request.method == "DELETE":
        return delete_tag_handler(tag_id)
# GET single tag
def get_single_tag(tag_id):
    tag = db.session.get(Tags, tag_id)
    if not tag:
        return jsonify({f"Error": f"Tag with id {tag_id} not found"}), 404
    return jsonify({"tagId": tag.tagId, "name": tag.name, "tagType": tag.tagType.name}), 200
    
# DELETE - delete tag    
def delete_tag_handler(tag_id):
    tag = db.session.get(Tags, tag_id)
    if not tag:
        return jsonify({"Error": f"Tag with id {tag_id} not found"}), 404

    try:
        db.session.delete(tag)
        db.session.commit()
        return jsonify({"message": f"Tag with id {tag_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return (
            jsonify({"Error": f"An error occured while deleting the tag: {str(e)}"}),
            500,
        )

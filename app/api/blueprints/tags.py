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
    try:
        tag_id = request.args.get("tagId")
        
        if tag_id:
            statement = select(Tags).where(Tags.tagId == tag_id)
        else:
            statement =select(Tags)
            
        with db.engine.connect() as conn:
            results = conn.execute(statement)
        
        response = []
        for result in results:
            tagId, name, tagType = result
            response.append({
                "tagId": tagId,
                "name": name,
                "tagType": tagType.name
            })
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"Error": str(e)})
       
# POST - create a new tag
def post_tags_handler():
    pass

# GET, PUT, DELETE - get/update/delete tags
@tags_blueprint.route("/<int:tag_id>", methods=["GET", "PUT", "DELETE"])
def update_delete_tags_handler(tag_id):
    if request.method == "GET":
        return get_tag_by_id(tag_id)
    elif request.method == "PUT":
        return update_tag_handler(tag_id)
    elif request.method == "DELETE":
        return delete_tag_handler(tag_id)
    return jsonify({"Error": "Invalid"}), 500

# GET - retrieve a specific tag
def get_tag_by_id(tag_id):
    try:
        statement = select(Tags).where(Tags.tagId == tag_id)
        with db.engine.connect() as conn:
            result = conn.execute(statement).fetchone()
            
        if not result:
            return jsonify({"Error": f"Tag with id {tag_id} not found"}), 404
        
        tagId, name, tagType = result
        return jsonify({
            "tagId": tagId,
            "name": name,
            "tagType": tagType.name
        }, 200)
    except Exception as e:
        return jsonify({"Error", str(e)})
    
# PUT - update tag
def update_tag_handler(tag_id: int):
    try:
        # Get data from request
        data = request.get_json()
        
        # Validate the input data
        if not data or not all(key in data for key in ["name", "tagType"]):
            return jsonify({"Error": "Missing required fields: name, tagType"}, 400)
        
        # Get tag from db
        tag = db.session.query(Tags).get(tag_id)
        
        if not tag:
            return jsonify({"Error": f"Tag with id {tag_id} not found."}, 404)
        
        # Handle tagType from string to enum
        tagType = TagType[data["tagType"]]
        
        # Update the tag field
        tag.name = data["name"]
        tag.tagType = tagType
        
        db.session.commit()
        
        return jsonify({
            "message": "Tag updated successfully",
            "tagId": tag.tagId,
            "name": tag.name,
            "tagType": tag.tagType.name
        }, 200)
    except KeyError:
        return jsonify({"Error": "Invalid tagType value"}, 400)
    except Exception as e:
        return jsonify({"Error": str(e)})
    
# DELETE - delete tag
def delete_tag_handler(tag_id: int):
    return(
        jsonify({"endpoint": "DELETE_tags_handler", "tagId": tag_id}, 200)
    )
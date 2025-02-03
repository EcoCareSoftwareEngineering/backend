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
    return(
        jsonify({"endpoint": "PUT_tags_handler", "tagId": tag_id}, 200)
    )
    
# DELETE - delete tag
def delete_tag_handler(tag_id: int):
    return(
        jsonify({"endpoint": "DELETE_tags_handler", "tagId": tag_id}, 200)
    )
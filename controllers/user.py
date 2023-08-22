from datetime import datetime

from factory import api, db
from factory import db
from flask import Blueprint, jsonify
from flask.globals import request
from models.user import User, UserCreate
from spectree import Response

user_controller = Blueprint("user_controller", __name__, url_prefix="/users")

@user_controller.get("/")
@api.validate(resp=Response(HTTP_200=None), tags=["users"])
def get_users():
    """
    Get all users
    """
    users = User.query.all()

    return jsonify(
        [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "birthdate": user.birthdate.isoformat() if user.birthdate else None,
                "created_at" : user.created_at.isoformat(),
            }
            for user in users
        ]
    ), 200


@user_controller.get("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=None, HTTP_404=None), tags=["users"])
def get_user(user_id):
    """
    Get a specified user
    """
    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "birthdate": user.birthdate.isoformat() if user.birthdate else None,
        "created_at" : user.created_at.isoformat(),
    }, 200


@user_controller.post("/")
@api.validate(resp=Response(HTTP_201=None), tags=["users"])
def post_user():
    """
    Create an user
    """
    data = request.json

    if User.query.filter_by(username=data["username"]).first():
        return {"msg": "username not available"}, 409
    
    if "birthdate" in data:
        if data["birthdate"].endswith("Z"):
            data["birthdate"] = data["birthdate"][:-1]

    user = User(
        username=data["username"], 
        email=data["email"],
        birthdate=datetime.fromisoformat(data["birthdate"]) 
        if "birthdate" in data 
        else None,
    )

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created successfully."}, 201


@user_controller.put("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=None, HTTP_404=None), tags=["users"])
def put_user(user_id):
    """
    Update an user
    """
    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    data = request.json

    if "birthdate" in data:
        if data["birthdate"].endswith("Z"):
            data["birthdate"] = data["birthdate"][:-1]
        user.birthdate = datetime.fromisoformat(data["birthdate"])

    user.username = data["username"]
    user.email = data["email"]

    db.session.commit()

    return {"msg": "User was updated."}, 200


@user_controller.delete("/<int:user_id>")
@api.validate(resp=Response(HTTP_200=None, HTTP_404=None), tags=["users"])
def delete_user(user_id):
    """
    Delete an user
    """
    user = User.query.get(user_id)

    if user is None:
        return {"msg": f"There is no user with id {user_id}"}, 404

    db.session.delete(user)
    db.session.commit()

    return {"msg": "User deleted from the database."}, 200

# Validação da rota
from factory import api
from pydantic import BaseModel
from spectree import Response

from flask import Blueprint, request

from flask_jwt_extended import create_access_token

# Modelo para buscar o usuário no banco de dados
from models import User

from utils.responses import DefaultResponse

auth_controller = Blueprint("auth_controller", __name__, url_prefix="/auth")


class LoginMessage(BaseModel):
    username: str
    password: str


class LoginResponseMessage(BaseModel):
    access_token: str


@auth_controller.post("/login")
@api.validate(
    json=LoginMessage,
    resp=Response(HTTP_200=LoginResponseMessage, HTTP_401=DefaultResponse),
    security={},
    tags=["auth"],
)
def login():
    """Login in the system"""

    data = request.json

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.verify_password(data["password"]):
        return {
            "access_token": create_access_token(
                identity=user.username, expires_delta=None
            )
        }

    return {"msg": "Username and password do not match."}, 401


@auth_controller.post("/logout")
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["auth"])
def logout():
    """Logout user"""

     #without the token, the client is no longer able to authenticate
    return {"msg": "Logout successfully."}


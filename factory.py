from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from spectree import SpecTree
from flask_jwt_extended import JWTManager

from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = SpecTree("flask", title="Mini Feed API", version="v.1.0", path="docs")

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    jwt.init_app(app)
    
    db.init_app(app)

    from models import User
    migrate.init_app(app, db)

    from controllers import user_controller, auth_controller

    app.register_blueprint(user_controller)
    app.register_blueprint(auth_controller)

    api.register(app)

    return app

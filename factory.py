from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from spectree import SpecTree

from config import Config

db = SQLAlchemy()
migrate = Migrate()
api = SpecTree("flask", title="Mini Feed API", version="v.1.0", path="docs")

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)

    from models import User
    migrate.init_app(app, db)

    from controllers import user_controller

    app.register_blueprint(user_controller)

    api.register(app)

    return app

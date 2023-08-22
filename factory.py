from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# Importamos a classe Migrate
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
# Criamos uma instância da classe Migrate
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    
    db.init_app(app)

    # Importamos os modelos criados
    from models import User

    # Inicializamos o Flask-Migrate com nossa aplicação
    migrate.init_app(app, db)

    @app.route("/")
    def hello_world():
        return "<h1>Hello, World!</h1>"

    return app

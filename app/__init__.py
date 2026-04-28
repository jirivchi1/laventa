from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.extensions import db, migrate, login_manager, mail, csrf


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Registrar blueprints
    from app.routes import register_blueprints
    register_blueprints(app)

    # Crear tablas si no existen (dev)
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()

    return app

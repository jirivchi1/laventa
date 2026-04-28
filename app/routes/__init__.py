from app.routes.main import main_bp
from app.routes.propiedades import propiedades_bp
from app.routes.reservas import reservas_bp
from app.routes.enoturismo import enoturismo_bp
from app.routes.eventos import eventos_bp
from app.routes.admin import admin_bp
from app.routes.limpieza import limpieza_bp
from app.routes.auth import auth_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(propiedades_bp, url_prefix='/propiedades')
    app.register_blueprint(reservas_bp, url_prefix='/reservas')
    app.register_blueprint(enoturismo_bp, url_prefix='/enoturismo')
    app.register_blueprint(eventos_bp, url_prefix='/eventos')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(limpieza_bp, url_prefix='/limpieza')
    app.register_blueprint(auth_bp, url_prefix='/auth')

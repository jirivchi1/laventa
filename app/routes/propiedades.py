from flask import Blueprint, render_template, abort

from app.models.propiedad import Propiedad

propiedades_bp = Blueprint('propiedades', __name__)


@propiedades_bp.route('/')
def listado():
    casas = Propiedad.query.filter_by(tipo='casa', activa=True).all()
    habitaciones = Propiedad.query.filter_by(tipo='habitacion', activa=True).all()
    return render_template('propiedades/listado.html',
                           casas=casas,
                           habitaciones=habitaciones)


@propiedades_bp.route('/<slug>')
def detalle(slug):
    propiedad = Propiedad.query.filter_by(slug=slug, activa=True).first()
    if not propiedad:
        abort(404)
    return render_template('propiedades/detalle.html', propiedad=propiedad)

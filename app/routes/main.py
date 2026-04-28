from flask import Blueprint, render_template, request, flash, redirect, url_for

from app.models.propiedad import Propiedad
from app.models.experiencia import Experiencia
from app.services.email_service import EmailService

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def inicio():
    casas = Propiedad.query.filter_by(tipo='casa', activa=True).all()
    habitaciones = Propiedad.query.filter_by(tipo='habitacion', activa=True).all()
    experiencias = Experiencia.query.filter_by(activa=True).limit(3).all()
    return render_template('main/inicio.html',
                           casas=casas,
                           habitaciones=habitaciones,
                           experiencias=experiencias)


@main_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'email': request.form.get('email'),
            'telefono': request.form.get('telefono'),
            'tipo_consulta': request.form.get('tipo_consulta'),
            'mensaje': request.form.get('mensaje'),
        }

        EmailService.enviar_contacto(datos)
        flash('Mensaje enviado correctamente. Te responderemos pronto.', 'success')
        return redirect(url_for('main.contacto'))

    return render_template('main/contacto.html')

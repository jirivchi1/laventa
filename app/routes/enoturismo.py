from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime

from app.extensions import db
from app.models.experiencia import Experiencia, ReservaExperiencia

enoturismo_bp = Blueprint('enoturismo', __name__)


@enoturismo_bp.route('/')
def listado():
    experiencias = Experiencia.query.filter_by(activa=True).all()
    return render_template('enoturismo/listado.html', experiencias=experiencias)


@enoturismo_bp.route('/reservar/<int:experiencia_id>', methods=['POST'])
def reservar(experiencia_id):
    experiencia = Experiencia.query.get_or_404(experiencia_id)

    try:
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
    except (ValueError, KeyError):
        flash('La fecha no es válida.', 'danger')
        return redirect(url_for('enoturismo.listado'))

    # Comprobar plazas disponibles
    reservas_dia = ReservaExperiencia.query.filter(
        ReservaExperiencia.experiencia_id == experiencia_id,
        ReservaExperiencia.fecha == fecha,
        ReservaExperiencia.estado.in_(['pendiente', 'confirmada'])
    ).all()
    personas_reservadas = sum(r.num_personas for r in reservas_dia)
    num_personas = int(request.form.get('num_personas', 1))

    if personas_reservadas + num_personas > experiencia.plazas_max:
        flash('No hay plazas suficientes para esa fecha.', 'danger')
        return redirect(url_for('enoturismo.listado'))

    reserva = ReservaExperiencia(
        experiencia_id=experiencia_id,
        fecha=fecha,
        nombre_cliente=request.form['nombre'],
        email_cliente=request.form['email'],
        telefono_cliente=request.form['telefono'],
        num_personas=num_personas,
    )
    db.session.add(reserva)
    db.session.commit()

    flash('Reserva de experiencia creada. Te contactaremos para confirmar.', 'success')
    return redirect(url_for('enoturismo.listado'))

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from datetime import datetime, date

from app.extensions import db
from app.models.propiedad import Propiedad
from app.models.reserva import Reserva
from app.services.reserva_service import ReservaService

reservas_bp = Blueprint('reservas', __name__)


@reservas_bp.route('/nueva/<int:propiedad_id>', methods=['GET', 'POST'])
def nueva(propiedad_id):
    propiedad = Propiedad.query.get_or_404(propiedad_id)

    if request.method == 'POST':
        try:
            fecha_entrada = datetime.strptime(request.form['fecha_entrada'], '%Y-%m-%d').date()
            fecha_salida = datetime.strptime(request.form['fecha_salida'], '%Y-%m-%d').date()
        except (ValueError, KeyError):
            flash('Las fechas no son válidas.', 'danger')
            return redirect(url_for('reservas.nueva', propiedad_id=propiedad_id))

        if fecha_salida <= fecha_entrada:
            flash('La fecha de salida debe ser posterior a la de entrada.', 'danger')
            return redirect(url_for('reservas.nueva', propiedad_id=propiedad_id))

        if fecha_entrada < date.today():
            flash('La fecha de entrada no puede ser anterior a hoy.', 'danger')
            return redirect(url_for('reservas.nueva', propiedad_id=propiedad_id))

        # Verificar disponibilidad
        if not ReservaService.esta_disponible(propiedad_id, fecha_entrada, fecha_salida):
            flash('La propiedad no está disponible en esas fechas.', 'danger')
            return redirect(url_for('reservas.nueva', propiedad_id=propiedad_id))

        reserva = Reserva(
            propiedad_id=propiedad_id,
            nombre_cliente=request.form['nombre'],
            email_cliente=request.form['email'],
            telefono_cliente=request.form['telefono'],
            num_personas=int(request.form['num_personas']),
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            precio_total=ReservaService.calcular_precio(propiedad, fecha_entrada, fecha_salida),
        )
        db.session.add(reserva)
        db.session.commit()

        # TODO: enviar email de confirmación
        flash('Reserva creada correctamente. Te enviaremos un email de confirmación.', 'success')
        return redirect(url_for('reservas.confirmacion', reserva_id=reserva.id))

    return render_template('reservas/nueva.html', propiedad=propiedad)


@reservas_bp.route('/confirmacion/<int:reserva_id>')
def confirmacion(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    return render_template('reservas/confirmacion.html', reserva=reserva)


@reservas_bp.route('/api/disponibilidad/<int:propiedad_id>')
def api_disponibilidad(propiedad_id):
    """Devuelve las fechas ocupadas para el calendario público."""
    reservas = Reserva.query.filter(
        Reserva.propiedad_id == propiedad_id,
        Reserva.estado.in_(['confirmada', 'pagada', 'pendiente'])
    ).all()

    fechas_ocupadas = []
    for r in reservas:
        fechas_ocupadas.append({
            'start': r.fecha_entrada.isoformat(),
            'end': r.fecha_salida.isoformat(),
            'display': 'background',
            'color': '#dc3545',
        })

    return jsonify(fechas_ocupadas)

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import datetime, date

from app.extensions import db
from app.models.reserva import Reserva
from app.models.propiedad import Propiedad
from app.models.experiencia import ReservaExperiencia

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@login_required
def require_admin():
    if not current_user.es_admin:
        abort(403)


@admin_bp.route('/')
def dashboard():
    hoy = date.today()

    reservas_pendientes = Reserva.query.filter_by(estado='pendiente').count()
    reservas_hoy = Reserva.query.filter(
        Reserva.fecha_entrada <= hoy,
        Reserva.fecha_salida >= hoy,
        Reserva.estado.in_(['confirmada', 'pagada'])
    ).all()
    total_propiedades = Propiedad.query.filter_by(activa=True).count()

    return render_template('admin/dashboard.html',
                           reservas_pendientes=reservas_pendientes,
                           reservas_hoy=reservas_hoy,
                           total_propiedades=total_propiedades)


@admin_bp.route('/reservas')
def reservas():
    estado = request.args.get('estado', 'todas')
    query = Reserva.query.order_by(Reserva.creada_en.desc())

    if estado != 'todas':
        query = query.filter_by(estado=estado)

    reservas = query.all()
    return render_template('admin/reservas.html', reservas=reservas, estado_filtro=estado)


@admin_bp.route('/reservas/<int:reserva_id>/estado', methods=['POST'])
def cambiar_estado_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    nuevo_estado = request.form.get('estado')

    if nuevo_estado in ['pendiente', 'confirmada', 'pagada', 'cancelada', 'completada']:
        reserva.estado = nuevo_estado
        db.session.commit()
        flash(f'Reserva #{reserva.id} actualizada a "{nuevo_estado}".', 'success')

    return redirect(url_for('admin.reservas'))


@admin_bp.route('/propiedades')
def propiedades():
    propiedades = Propiedad.query.all()
    return render_template('admin/propiedades.html', propiedades=propiedades)

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date

from app.extensions import db
from app.models.reserva import Reserva
from app.models.propiedad import Propiedad
from app.models.experiencia import ReservaExperiencia

admin_bp = Blueprint('admin', __name__)

# Colores para distinguir propiedades en el calendario
COLORES_PROPIEDADES = [
    '#4e79a7', '#f28e2b', '#e15759', '#76b7b2',
    '#59a14f', '#edc948', '#b07aa1', '#ff9da7',
    '#9c755f', '#bab0ac',
]


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


@admin_bp.route('/calendario')
def calendario():
    propiedades = Propiedad.query.filter_by(activa=True).all()

    # Asignar color a cada propiedad
    leyenda = []
    for i, p in enumerate(propiedades):
        leyenda.append({
            'id': p.id,
            'nombre': p.nombre,
            'color': COLORES_PROPIEDADES[i % len(COLORES_PROPIEDADES)],
        })

    return render_template('admin/calendario.html', leyenda=leyenda)


@admin_bp.route('/api/calendario')
def api_calendario():
    """Devuelve todas las reservas activas para el calendario del admin."""
    propiedad_id = request.args.get('propiedad_id', type=int)

    query = Reserva.query.filter(
        Reserva.estado.in_(['pendiente', 'confirmada', 'pagada'])
    )

    if propiedad_id:
        query = query.filter_by(propiedad_id=propiedad_id)

    reservas = query.all()

    # Mapear colores por propiedad
    propiedades = Propiedad.query.all()
    colores = {}
    for i, p in enumerate(propiedades):
        colores[p.id] = COLORES_PROPIEDADES[i % len(COLORES_PROPIEDADES)]

    # Colores de borde según estado
    bordes_estado = {
        'pendiente': '#ffc107',
        'confirmada': '#198754',
        'pagada': '#0d6efd',
    }

    eventos = []
    for r in reservas:
        eventos.append({
            'id': r.id,
            'title': f'{r.propiedad.nombre} - {r.nombre_cliente}',
            'start': r.fecha_entrada.isoformat(),
            'end': r.fecha_salida.isoformat(),
            'color': colores.get(r.propiedad_id, '#6c757d'),
            'borderColor': bordes_estado.get(r.estado, '#6c757d'),
            'extendedProps': {
                'reserva_id': r.id,
                'propiedad': r.propiedad.nombre,
                'cliente': r.nombre_cliente,
                'email': r.email_cliente,
                'telefono': r.telefono_cliente,
                'personas': r.num_personas,
                'noches': r.num_noches,
                'estado': r.estado,
                'estado_limpieza': r.estado_limpieza,
                'precio': r.precio_total,
            },
        })

    return jsonify(eventos)


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

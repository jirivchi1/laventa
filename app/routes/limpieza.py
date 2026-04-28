from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from datetime import date, timedelta

from app.extensions import db
from app.models.reserva import Reserva
from app.models.propiedad import Propiedad

limpieza_bp = Blueprint('limpieza', __name__)


@limpieza_bp.before_request
@login_required
def require_limpieza():
    if not current_user.es_limpieza:
        abort(403)


@limpieza_bp.route('/')
def dashboard():
    hoy = date.today()
    manana = hoy + timedelta(days=1)
    en_30_dias = hoy + timedelta(days=30)

    # Salidas de hoy: necesitan limpieza
    salidas_hoy = Reserva.query.filter(
        Reserva.fecha_salida == hoy,
        Reserva.estado.in_(['confirmada', 'pagada', 'completada'])
    ).all()

    # Entradas de hoy: deben estar listas
    entradas_hoy = Reserva.query.filter(
        Reserva.fecha_entrada == hoy,
        Reserva.estado.in_(['confirmada', 'pagada'])
    ).all()

    # Entradas de mañana: preparar con antelación
    entradas_manana = Reserva.query.filter(
        Reserva.fecha_entrada == manana,
        Reserva.estado.in_(['confirmada', 'pagada'])
    ).all()

    # Tareas de limpieza pendientes (de reservas recientes)
    pendientes = Reserva.query.filter(
        Reserva.estado_limpieza.in_(['pendiente', 'en_proceso']),
        Reserva.fecha_salida <= hoy,
        Reserva.estado.in_(['confirmada', 'pagada', 'completada'])
    ).order_by(Reserva.fecha_salida.asc()).all()

    # Próximas estancias confirmadas (excluye hoy y mañana, ya mostradas arriba)
    proximas = Reserva.query.filter(
        Reserva.fecha_entrada > manana,
        Reserva.fecha_entrada <= en_30_dias,
        Reserva.estado.in_(['confirmada', 'pagada'])
    ).order_by(Reserva.fecha_entrada.asc()).all()

    return render_template('limpieza/dashboard.html',
                           hoy=hoy,
                           salidas_hoy=salidas_hoy,
                           entradas_hoy=entradas_hoy,
                           entradas_manana=entradas_manana,
                           pendientes=pendientes,
                           proximas=proximas)


@limpieza_bp.route('/tareas')
def tareas():
    hoy = date.today()
    filtro = request.args.get('filtro', 'pendientes')

    # Base: solo reservas confirmadas (admin las ha aprobado)
    query = Reserva.query.filter(
        Reserva.estado.in_(['confirmada', 'pagada', 'completada'])
    )

    if filtro == 'pendientes':
        # Limpieza pendiente y la salida ya pasó (o es hoy)
        query = query.filter(
            Reserva.fecha_salida <= hoy,
            Reserva.estado_limpieza.in_(['pendiente', 'en_proceso']),
        )
    elif filtro == 'completadas':
        query = query.filter_by(estado_limpieza='completada')
    elif filtro == 'proximas':
        # Reservas futuras (planificación)
        query = query.filter(Reserva.fecha_entrada >= hoy)
    # 'todas' no añade filtros extra

    tareas = query.order_by(Reserva.fecha_salida.desc()).all()

    return render_template('limpieza/tareas.html',
                           tareas=tareas,
                           filtro=filtro)


@limpieza_bp.route('/tareas/<int:reserva_id>/estado', methods=['POST'])
def cambiar_estado_limpieza(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)
    nuevo_estado = request.form.get('estado_limpieza')

    if nuevo_estado in ['pendiente', 'en_proceso', 'completada']:
        reserva.estado_limpieza = nuevo_estado
        db.session.commit()
        flash(f'Limpieza de {reserva.propiedad.nombre} actualizada a "{nuevo_estado}".', 'success')

    return redirect(request.referrer or url_for('limpieza.dashboard'))


@limpieza_bp.route('/calendario')
def calendario():
    """Vista semanal simplificada de entradas y salidas."""
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo

    # Offset para navegar semanas
    offset = request.args.get('semana', 0, type=int)
    inicio_semana += timedelta(weeks=offset)
    fin_semana += timedelta(weeks=offset)

    # Reservas que tocan esta semana
    reservas = Reserva.query.filter(
        Reserva.fecha_entrada <= fin_semana,
        Reserva.fecha_salida >= inicio_semana,
        Reserva.estado.in_(['confirmada', 'pagada', 'completada'])
    ).order_by(Reserva.fecha_entrada).all()

    # Armar días de la semana
    dias = []
    for i in range(7):
        dia = inicio_semana + timedelta(days=i)
        entradas = [r for r in reservas if r.fecha_entrada == dia]
        salidas = [r for r in reservas if r.fecha_salida == dia]
        dias.append({
            'fecha': dia,
            'entradas': entradas,
            'salidas': salidas,
        })

    return render_template('limpieza/calendario.html',
                           dias=dias,
                           offset=offset,
                           hoy=hoy,
                           inicio_semana=inicio_semana,
                           fin_semana=fin_semana)

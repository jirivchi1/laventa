from flask import Blueprint, render_template, request, flash, redirect, url_for

eventos_bp = Blueprint('eventos', __name__)

SALONES = [
    {
        'id': 'cocina-campera',
        'nombre': 'Cocina Campera',
        'capacidad': 30,
        'descripcion': 'Salón con chimenea, cocina office y barbacoa exterior. Ideal para reuniones íntimas.',
    },
    {
        'id': 'salon-estrella',
        'nombre': 'Salón Estrella',
        'capacidad': 70,
        'descripcion': 'Salón amplio con cocina profesional para catering. Perfecto para celebraciones medianas.',
    },
    {
        'id': 'salon-invernadero',
        'nombre': 'Salón Invernadero',
        'capacidad': 300,
        'descripcion': 'Gran salón independiente con entrada propia y cocina profesional. Para grandes eventos y bodas.',
    },
]


@eventos_bp.route('/')
def salones():
    return render_template('eventos/salones.html', salones=SALONES)


@eventos_bp.route('/solicitar', methods=['POST'])
def solicitar():
    # Recibe solicitud de presupuesto para evento
    datos = {
        'nombre': request.form.get('nombre'),
        'email': request.form.get('email'),
        'telefono': request.form.get('telefono'),
        'salon': request.form.get('salon'),
        'tipo_evento': request.form.get('tipo_evento'),
        'fecha': request.form.get('fecha'),
        'num_personas': request.form.get('num_personas'),
        'mensaje': request.form.get('mensaje'),
    }

    # TODO: enviar email al admin con la solicitud
    flash('Solicitud de presupuesto enviada. Te contactaremos en menos de 24 horas.', 'success')
    return redirect(url_for('eventos.salones'))

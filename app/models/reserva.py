from datetime import datetime

from app.extensions import db


class Reserva(db.Model):
    """Reserva de una propiedad (casa o habitación)."""
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedades.id'), nullable=False)

    # Datos del cliente
    nombre_cliente = db.Column(db.String(100), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    telefono_cliente = db.Column(db.String(20), nullable=False)
    num_personas = db.Column(db.Integer, nullable=False)

    # Fechas
    fecha_entrada = db.Column(db.Date, nullable=False)
    fecha_salida = db.Column(db.Date, nullable=False)

    # Estado y pago
    estado = db.Column(db.String(20), default='pendiente')
    # Estados: pendiente, confirmada, pagada, cancelada, completada
    precio_total = db.Column(db.Float)
    notas = db.Column(db.Text)

    # Limpieza
    estado_limpieza = db.Column(db.String(20), default='pendiente')
    # Estados: pendiente, en_proceso, completada

    # Timestamps
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def num_noches(self):
        return (self.fecha_salida - self.fecha_entrada).days

    def __repr__(self):
        return f'<Reserva {self.id} - {self.nombre_cliente}>'

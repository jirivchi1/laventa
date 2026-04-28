from datetime import datetime

from app.extensions import db


class Experiencia(db.Model):
    """Experiencia de enoturismo (cata, visita bodega, etc.)."""
    __tablename__ = 'experiencias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    precio_alojado = db.Column(db.Float)  # Precio reducido para huéspedes
    duracion_minutos = db.Column(db.Integer)
    plazas_max = db.Column(db.Integer, nullable=False)
    dia_semana = db.Column(db.String(20))  # 'sabado', 'domingo', etc.
    hora = db.Column(db.String(5))  # '12:00'
    activa = db.Column(db.Boolean, default=True)

    reservas = db.relationship('ReservaExperiencia', backref='experiencia', lazy=True)

    def __repr__(self):
        return f'<Experiencia {self.nombre}>'


class ReservaExperiencia(db.Model):
    """Reserva de una experiencia de enoturismo."""
    __tablename__ = 'reservas_experiencias'

    id = db.Column(db.Integer, primary_key=True)
    experiencia_id = db.Column(db.Integer, db.ForeignKey('experiencias.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    # Datos del cliente
    nombre_cliente = db.Column(db.String(100), nullable=False)
    email_cliente = db.Column(db.String(120), nullable=False)
    telefono_cliente = db.Column(db.String(20), nullable=False)
    num_personas = db.Column(db.Integer, nullable=False)

    estado = db.Column(db.String(20), default='pendiente')
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ReservaExperiencia {self.id}>'

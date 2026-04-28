from app.extensions import db


class Propiedad(db.Model):
    """Casa rural o habitación disponible para reservar."""
    __tablename__ = 'propiedades'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'casa' o 'habitacion'
    descripcion = db.Column(db.Text)
    capacidad = db.Column(db.Integer, nullable=False)
    precio_noche = db.Column(db.Float, nullable=False)
    caracteristicas = db.Column(db.Text)  # JSON string con lista de características
    activa = db.Column(db.Boolean, default=True)

    imagenes = db.relationship('ImagenPropiedad', backref='propiedad', lazy=True)
    reservas = db.relationship('Reserva', backref='propiedad', lazy=True)

    def __repr__(self):
        return f'<Propiedad {self.nombre}>'


class ImagenPropiedad(db.Model):
    __tablename__ = 'imagenes_propiedad'

    id = db.Column(db.Integer, primary_key=True)
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedades.id'), nullable=False)
    ruta = db.Column(db.String(256), nullable=False)
    es_principal = db.Column(db.Boolean, default=False)

"""
Script para poblar la base de datos con los datos iniciales del negocio.
Ejecutar: python seed.py
"""
from app import create_app
from app.extensions import db
from app.models.usuario import Usuario
from app.models.propiedad import Propiedad
from app.models.experiencia import Experiencia

app = create_app()

with app.app_context():
    # Crear tablas
    db.create_all()

    # --- Usuario admin ---
    if not Usuario.query.filter_by(email='admin@laventadelasestrellas.com').first():
        admin = Usuario(
            nombre='Administrador',
            email='admin@laventadelasestrellas.com',
            es_admin=True,
        )
        admin.set_password('admin123')  # CAMBIAR en producción
        db.session.add(admin)
        print('Usuario admin creado.')

    # --- Casas rurales ---
    casas = [
        {
            'nombre': 'Casa Tempranillo',
            'slug': 'casa-tempranillo',
            'tipo': 'casa',
            'descripcion': 'Ideal para familias numerosas. Casa completa con climatización, estufa de leña, cocina equipada, barbacoa y porche privado.',
            'capacidad': 8,
            'precio_noche': 120,
            'caracteristicas': 'Climatización,Estufa de leña,Cocina equipada,Barbacoa,Porche privado,WiFi',
        },
        {
            'nombre': 'Casa Airén',
            'slug': 'casa-airen',
            'tipo': 'casa',
            'descripcion': 'Perfecta para parejas y familias reducidas. Acogedora y con todas las comodidades necesarias.',
            'capacidad': 4,
            'precio_noche': 85,
            'caracteristicas': 'Climatización,Cocina equipada,Salón con chimenea,Porche,WiFi',
        },
        {
            'nombre': 'Casa Luna',
            'slug': 'casa-luna',
            'tipo': 'casa',
            'descripcion': 'Amplia y confortable, ideal para dos parejas o familia. Ubicada en primera planta con vistas a los viñedos.',
            'capacidad': 4,
            'precio_noche': 90,
            'caracteristicas': 'Climatización,Cocina equipada,Vistas a viñedos,Terraza,WiFi',
        },
        {
            'nombre': 'Casa Lucero',
            'slug': 'casa-lucero',
            'tipo': 'casa',
            'descripcion': 'Idónea para grupos jóvenes. Ambiente moderno con chimenea integrada y zona de relax.',
            'capacidad': 6,
            'precio_noche': 100,
            'caracteristicas': 'Climatización,Chimenea integrada,Cocina equipada,Zona relax,WiFi',
        },
    ]

    for datos in casas:
        if not Propiedad.query.filter_by(slug=datos['slug']).first():
            db.session.add(Propiedad(**datos))
            print(f"Casa creada: {datos['nombre']}")

    # --- Habitaciones ---
    habitaciones = [
        {
            'nombre': 'Habitación Cosmos',
            'slug': 'habitacion-cosmos',
            'tipo': 'habitacion',
            'descripcion': 'Habitación doble con baño privado. Acceso a salón social con café e infusiones.',
            'capacidad': 2,
            'precio_noche': 55,
            'caracteristicas': 'Baño privado,Climatización,Salón social,Café e infusiones,WiFi',
        },
        {
            'nombre': 'Habitación Conuco',
            'slug': 'habitacion-conuco',
            'tipo': 'habitacion',
            'descripcion': 'Habitación doble con vistas a la finca. Baño privado y acceso a zonas comunes.',
            'capacidad': 2,
            'precio_noche': 55,
            'caracteristicas': 'Baño privado,Climatización,Vistas a la finca,Salón social,WiFi',
        },
        {
            'nombre': 'Habitación Dionisos',
            'slug': 'habitacion-dionisos',
            'tipo': 'habitacion',
            'descripcion': 'Habitación triple amplia. Ideal para familias pequeñas o grupo de amigos.',
            'capacidad': 3,
            'precio_noche': 70,
            'caracteristicas': 'Baño privado,Climatización,Capacidad triple,Salón social,WiFi',
        },
    ]

    for datos in habitaciones:
        if not Propiedad.query.filter_by(slug=datos['slug']).first():
            db.session.add(Propiedad(**datos))
            print(f"Habitación creada: {datos['nombre']}")

    # --- Experiencias de enoturismo ---
    experiencias = [
        {
            'nombre': 'Visita con cata de vinos',
            'slug': 'visita-cata-vinos',
            'descripcion': 'Visita a La Bodega de las Estrellas con cata de 5 vinos naturales y 3 tapas. Recorrido por los viñedos ecológicos y la bodega.',
            'precio': 18,
            'precio_alojado': 15,
            'duracion_minutos': 120,
            'plazas_max': 20,
            'dia_semana': 'sábado',
            'hora': '12:00',
        },
        {
            'nombre': 'Experiencia inmersiva de vendimia',
            'slug': 'experiencia-vendimia',
            'descripcion': 'Participa en la vendimia, aprende sobre el cultivo ecológico y el calendario cósmico aplicado a los viñedos. Incluye comida entre viñedos.',
            'precio': 35,
            'precio_alojado': 30,
            'duracion_minutos': 240,
            'plazas_max': 12,
            'dia_semana': 'sábado',
            'hora': '10:00',
        },
    ]

    for datos in experiencias:
        if not Experiencia.query.filter_by(slug=datos['slug']).first():
            db.session.add(Experiencia(**datos))
            print(f"Experiencia creada: {datos['nombre']}")

    db.session.commit()
    print('\nDatos iniciales cargados correctamente.')

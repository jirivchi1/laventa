# La Venta de las Estrellas

Aplicación web para la gestión de reservas, enoturismo y eventos de [La Venta de las Estrellas](https://www.laventadelasestrellas.com/), complejo rural en Valdepeñas (Ciudad Real).

## Stack

- **Backend:** Python 3 + Flask
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend:** Jinja2 + Bootstrap 5
- **Calendario:** FullCalendar.js

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/jirivchi1/laventa.git
cd laventa

# Entorno virtual
python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash)
# source venv/bin/activate      # Linux / Mac
pip install -r requirements.txt

# Configuración
cp .env.example .env
# Editar .env con tus valores (SECRET_KEY, email, etc.)

# Crear base de datos con datos iniciales
python seed.py

# Arrancar servidor de desarrollo
python run.py
```

El servidor arranca en `http://localhost:5000`.

## Acceso admin

```
URL:        http://localhost:5000/auth/login
Email:      admin@laventadelasestrellas.com
Contraseña: admin123
```

> Cambiar la contraseña del admin antes de desplegar en producción.

## Estructura del proyecto

```
app/
├── models/       # Modelos de base de datos (SQLAlchemy)
├── routes/       # Rutas organizadas por blueprint
├── services/     # Lógica de negocio (reservas, email)
├── templates/    # Plantillas Jinja2 (Bootstrap 5)
├── static/       # CSS, JS, imágenes
├── config.py     # Configuración (variables de entorno)
└── extensions.py # Extensiones Flask (db, login, mail, csrf)
```

## Funcionalidades

- Listado de casas rurales y habitaciones con precios
- Sistema de reservas con calendario de disponibilidad
- Reserva de experiencias de enoturismo (catas, vendimia)
- Solicitud de presupuesto para eventos y salones
- Panel de administración con gestión de reservas
- Formulario de contacto con tipo de consulta

## Despliegue en producción

```bash
# Configurar PostgreSQL en .env
DATABASE_URL=postgresql://usuario:password@localhost:5432/venta_estrellas

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

## Licencia

Proyecto privado. Todos los derechos reservados.

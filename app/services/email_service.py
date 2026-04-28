from flask import current_app
from flask_mail import Message

from app.extensions import mail


class EmailService:

    @staticmethod
    def enviar_confirmacion_reserva(reserva):
        """Envía email de confirmación al cliente."""
        msg = Message(
            subject=f'Confirmación de reserva - {current_app.config["NOMBRE_NEGOCIO"]}',
            recipients=[reserva.email_cliente],
        )
        msg.body = f"""
Hola {reserva.nombre_cliente},

Tu reserva ha sido recibida:

- Propiedad: {reserva.propiedad.nombre}
- Entrada: {reserva.fecha_entrada.strftime('%d/%m/%Y')}
- Salida: {reserva.fecha_salida.strftime('%d/%m/%Y')}
- Personas: {reserva.num_personas}
- Precio total: {reserva.precio_total:.2f} EUR

Te confirmaremos la disponibilidad en breve.

Un saludo,
{current_app.config['NOMBRE_NEGOCIO']}
Tel: {current_app.config['TELEFONO']}
"""
        mail.send(msg)

    @staticmethod
    def enviar_aviso_admin(reserva):
        """Avisa al admin de una nueva reserva."""
        msg = Message(
            subject=f'Nueva reserva #{reserva.id} - {reserva.nombre_cliente}',
            recipients=[current_app.config['EMAIL_CONTACTO']],
        )
        msg.body = f"""
Nueva reserva recibida:

- Cliente: {reserva.nombre_cliente}
- Email: {reserva.email_cliente}
- Teléfono: {reserva.telefono_cliente}
- Propiedad: {reserva.propiedad.nombre}
- Entrada: {reserva.fecha_entrada.strftime('%d/%m/%Y')}
- Salida: {reserva.fecha_salida.strftime('%d/%m/%Y')}
- Personas: {reserva.num_personas}
- Precio: {reserva.precio_total:.2f} EUR

Accede al panel de administración para gestionar la reserva.
"""
        mail.send(msg)

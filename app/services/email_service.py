from flask import current_app, render_template
from flask_mail import Message

from app.extensions import mail


class EmailService:
    """Servicio de envío de emails.

    Todos los métodos capturan excepciones para no interrumpir
    el flujo del usuario si el envío falla.
    """

    @staticmethod
    def _enviar(destinatarios, asunto, template, **kwargs):
        """Método base para enviar un email con template HTML + texto plano."""
        try:
            html = render_template(template, **kwargs)

            msg = Message(
                subject=asunto,
                recipients=destinatarios,
            )
            msg.html = html
            # Texto plano como fallback (extraer de kwargs)
            msg.body = kwargs.get('texto_plano', '')

            mail.send(msg)
            current_app.logger.info(f'Email enviado a {destinatarios}: {asunto}')
            return True

        except Exception as e:
            current_app.logger.error(f'Error enviando email a {destinatarios}: {e}')
            return False

    # ===========================================
    # RESERVAS DE ALOJAMIENTO
    # ===========================================

    @staticmethod
    def confirmar_reserva(reserva):
        """Envía confirmación al cliente y aviso al admin."""
        email_admin = current_app.config['EMAIL_CONTACTO']
        negocio = current_app.config['NOMBRE_NEGOCIO']

        texto_cliente = (
            f'Hola {reserva.nombre_cliente},\n\n'
            f'Hemos recibido tu reserva #{reserva.id}:\n'
            f'- Alojamiento: {reserva.propiedad.nombre}\n'
            f'- Entrada: {reserva.fecha_entrada.strftime("%d/%m/%Y")}\n'
            f'- Salida: {reserva.fecha_salida.strftime("%d/%m/%Y")}\n'
            f'- Noches: {reserva.num_noches}\n'
            f'- Personas: {reserva.num_personas}\n'
            f'- Precio total: {reserva.precio_total:.2f} EUR\n\n'
            f'Te confirmaremos la disponibilidad en breve.\n\n'
            f'Un saludo,\n{negocio}'
        )

        texto_admin = (
            f'Nueva reserva #{reserva.id}\n'
            f'Cliente: {reserva.nombre_cliente}\n'
            f'Email: {reserva.email_cliente}\n'
            f'Telefono: {reserva.telefono_cliente}\n'
            f'Alojamiento: {reserva.propiedad.nombre}\n'
            f'Entrada: {reserva.fecha_entrada.strftime("%d/%m/%Y")}\n'
            f'Salida: {reserva.fecha_salida.strftime("%d/%m/%Y")}\n'
            f'Personas: {reserva.num_personas}\n'
            f'Precio: {reserva.precio_total:.2f} EUR'
        )

        # Email al cliente
        EmailService._enviar(
            [reserva.email_cliente],
            f'Confirmacion de reserva #{reserva.id} - {negocio}',
            'emails/reserva_cliente.html',
            reserva=reserva,
            texto_plano=texto_cliente,
        )

        # Email al admin
        EmailService._enviar(
            [email_admin],
            f'Nueva reserva #{reserva.id} - {reserva.nombre_cliente}',
            'emails/reserva_admin.html',
            reserva=reserva,
            texto_plano=texto_admin,
        )

    # ===========================================
    # RESERVAS DE EXPERIENCIAS
    # ===========================================

    @staticmethod
    def confirmar_experiencia(reserva):
        """Envía confirmación al cliente y aviso al admin para experiencia."""
        email_admin = current_app.config['EMAIL_CONTACTO']
        negocio = current_app.config['NOMBRE_NEGOCIO']

        texto_cliente = (
            f'Hola {reserva.nombre_cliente},\n\n'
            f'Hemos recibido tu reserva para: {reserva.experiencia.nombre}\n'
            f'- Fecha: {reserva.fecha.strftime("%d/%m/%Y")}\n'
            f'- Personas: {reserva.num_personas}\n\n'
            f'Te contactaremos para confirmar tu plaza.\n\n'
            f'Un saludo,\n{negocio}'
        )

        texto_admin = (
            f'Nueva reserva de experiencia\n'
            f'Experiencia: {reserva.experiencia.nombre}\n'
            f'Fecha: {reserva.fecha.strftime("%d/%m/%Y")}\n'
            f'Cliente: {reserva.nombre_cliente}\n'
            f'Email: {reserva.email_cliente}\n'
            f'Telefono: {reserva.telefono_cliente}\n'
            f'Personas: {reserva.num_personas}'
        )

        EmailService._enviar(
            [reserva.email_cliente],
            f'Reserva de experiencia - {negocio}',
            'emails/experiencia_cliente.html',
            reserva=reserva,
            texto_plano=texto_cliente,
        )

        EmailService._enviar(
            [email_admin],
            f'Nueva reserva experiencia - {reserva.nombre_cliente}',
            'emails/experiencia_admin.html',
            reserva=reserva,
            texto_plano=texto_admin,
        )

    # ===========================================
    # CONTACTO
    # ===========================================

    @staticmethod
    def enviar_contacto(datos):
        """Envía mensaje de contacto al admin."""
        email_admin = current_app.config['EMAIL_CONTACTO']

        texto_admin = (
            f'Nuevo mensaje de contacto\n'
            f'Nombre: {datos["nombre"]}\n'
            f'Email: {datos["email"]}\n'
            f'Telefono: {datos.get("telefono", "-")}\n'
            f'Tipo: {datos.get("tipo_consulta", "-")}\n'
            f'Mensaje: {datos["mensaje"]}'
        )

        return EmailService._enviar(
            [email_admin],
            f'Contacto web - {datos["nombre"]}',
            'emails/contacto_admin.html',
            datos=datos,
            texto_plano=texto_admin,
        )

    # ===========================================
    # EVENTOS
    # ===========================================

    @staticmethod
    def enviar_solicitud_evento(datos):
        """Envía solicitud de presupuesto al admin."""
        email_admin = current_app.config['EMAIL_CONTACTO']

        texto_admin = (
            f'Solicitud de presupuesto\n'
            f'Nombre: {datos["nombre"]}\n'
            f'Email: {datos["email"]}\n'
            f'Telefono: {datos["telefono"]}\n'
            f'Salon: {datos.get("salon", "-")}\n'
            f'Tipo evento: {datos.get("tipo_evento", "-")}\n'
            f'Fecha: {datos.get("fecha", "-")}\n'
            f'Personas: {datos.get("num_personas", "-")}\n'
            f'Mensaje: {datos.get("mensaje", "-")}'
        )

        return EmailService._enviar(
            [email_admin],
            f'Solicitud evento - {datos["nombre"]}',
            'emails/evento_admin.html',
            datos=datos,
            texto_plano=texto_admin,
        )

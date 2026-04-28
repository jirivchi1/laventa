from datetime import date

from app.models.reserva import Reserva


class ReservaService:

    @staticmethod
    def esta_disponible(propiedad_id, fecha_entrada, fecha_salida):
        """Comprueba si una propiedad está disponible entre dos fechas."""
        conflictos = Reserva.query.filter(
            Reserva.propiedad_id == propiedad_id,
            Reserva.estado.in_(['pendiente', 'confirmada', 'pagada']),
            Reserva.fecha_entrada < fecha_salida,
            Reserva.fecha_salida > fecha_entrada,
        ).count()
        return conflictos == 0

    @staticmethod
    def calcular_precio(propiedad, fecha_entrada, fecha_salida):
        """Calcula el precio total de la estancia."""
        num_noches = (fecha_salida - fecha_entrada).days
        if num_noches <= 0:
            return 0
        return propiedad.precio_noche * num_noches

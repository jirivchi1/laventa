from unicodedata import normalize
import re


def crear_slug(texto):
    """Convierte texto a slug URL-friendly: 'Casa Tempranillo' -> 'casa-tempranillo'"""
    texto = normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    texto = texto.lower().strip()
    texto = re.sub(r'[^a-z0-9]+', '-', texto)
    return texto.strip('-')


def formato_precio(precio):
    """Formatea precio: 85.0 -> '85,00 €'"""
    return f'{precio:,.2f} €'.replace(',', 'X').replace('.', ',').replace('X', '.')

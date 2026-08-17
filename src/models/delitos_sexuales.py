"""
Modelo de datos para el dataset de delitos sexuales.

Este módulo no ejecuta lógica de procesamiento. Define la estructura
esperada de los datos obtenidos desde la API de Datos Colombia y permite
detectar cambios en la estructura del dataset.
"""

from dataclasses import dataclass

@dataclass
class DelitoSexual:
    departamento: str
    municipio: str
    codigo_dane: str
    armas_medios: str
    fecha_hecho: str
    genero: str
    grupo_etario: str
    cantidad: int
    delito: str


COLUMNAS_ESPERADAS = [
    "departamento", "municipio", "codigo_dane", "armas_medios",
    "fecha_hecho", "genero", "grupo_etario", "cantidad", "delito",
]

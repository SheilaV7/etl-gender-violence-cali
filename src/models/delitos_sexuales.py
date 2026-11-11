"""
Modelo de datos para el dataset de delitos sexuales.

Este módulo no ejecuta lógica de procesamiento. Define la estructura
esperada de los datos obtenidos desde la API de Datos Colombia y permite
detectar cambios en la estructura del dataset.
"""

from dataclasses import dataclass


@dataclass
class DelitoSexual:
    municipio: str
    codigo_dane: str
    armas_medios: str
    anio: int
    mes: int
    dia_semana: str
    genero: str
    grupo_etario: str
    delito: str


COLUMNAS_ESPERADAS = [
    "municipio", "codigo_dane", "armas_medios", "anio", "mes",
    "dia_semana", "genero", "grupo_etario", "delito",
]

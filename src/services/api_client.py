"""
Módulo encargado de la comunicación con la API de Datos Colombia.

Responsabilidades:
- Realizar solicitudes HTTP.
- Obtener datasets mediante la API Socrata.
- Devolver los datos en formato JSON.
"""

import requests

class DatosGovClient:
    BASE_URL = "https://www.datos.gov.co/resource"

    def get_dataset(self, dataset_id: str, params: dict = None):
        url = f"{self.BASE_URL}/{dataset_id}.json"

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

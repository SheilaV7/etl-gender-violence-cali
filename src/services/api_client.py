"""
Módulo encargado de la comunicación con la API de Datos Colombia.

Responsabilidades:
- Realizar solicitudes HTTP.
- Obtener datasets mediante la API Socrata.
- Obtener metadatos de los datasets (columnas, tipos, fecha de actualización).
- Devolver los datos en formato JSON.
"""

import requests

class DatosGovClient:
    BASE_URL = "https://www.datos.gov.co/resource"
    METADATA_URL = "https://www.datos.gov.co/api/views"

    def get_dataset(self, dataset_id: str, params: dict = None):
        url = f"{self.BASE_URL}/{dataset_id}.json"

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_metadata(self, dataset_id: str):
        url = f"{self.METADATA_URL}/{dataset_id}.json"

        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    def get_columns(self, dataset_id: str):
        metadata = self.get_metadata(dataset_id)

        return [
            {
                "nombre": columna.get("fieldName"),
                "tipo": columna.get("dataTypeName"),
                "descripcion": columna.get("description"),
            }
            for columna in metadata.get("columns", [])
        ]

    def get_last_update(self, dataset_id: str):
        metadata = self.get_metadata(dataset_id)

        return {
            "datos_actualizados": metadata.get("rowsUpdatedAt"),
            "metadatos_actualizados": metadata.get("metadataUpdatedAt"),
        }

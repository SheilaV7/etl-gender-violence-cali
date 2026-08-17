"""
Módulo encargado de la paginación de resultados de la API de Datos Colombia.

Responsabilidades:
- Recorrer un dataset completo, página por página.
- Combinar los resultados en una sola lista.

Los parámetros $limit y $offset son administrados internamente
por el paginador y no deben proporcionarse en `params`.
"""

from services.api_client import DatosGovClient

class DatosGovPaginator:
    DEFAULT_PAGE_SIZE = 1000

    def __init__(self, client: DatosGovClient = None, page_size: int = None):
        self.client = client or DatosGovClient()
        self.page_size = page_size or self.DEFAULT_PAGE_SIZE

    def get_all(self, dataset_id: str, params: dict = None) -> list:
        params = dict(params or {})
        offset = 0
        resultados = []

        while True:
            params["$limit"] = self.page_size
            params["$offset"] = offset

            pagina = self.client.get_dataset(dataset_id, params)

            if not pagina:
                break

            resultados.extend(pagina)
            # print(f"  Página descargada: {len(pagina)} registros (total acumulado: {len(resultados)})")

            if len(pagina) < self.page_size:
                break  # última página, no hace falta seguir pidiendo

            offset += self.page_size

        return resultados

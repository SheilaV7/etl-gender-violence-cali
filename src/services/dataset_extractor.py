"""
Servicio encargado de extraer los datasets definidos en el catálogo
de Datos Abiertos Colombia.
"""

import pandas as pd

from config.datasets import DATASETS, DatasetConfig
from services.pagination import DatosGovPaginator

class DatasetExtractor:
    """Coordina la extracción de datasets mediante el paginador."""

    def __init__(self, paginator: DatosGovPaginator | None = None):
        self.paginator = paginator or DatosGovPaginator()

    def extract(self, config: DatasetConfig) -> pd.DataFrame:
        """
        Extrae un dataset y lo convierte en un DataFrame.

        Args:
            config: Configuración del dataset a extraer.

        Returns:
            DataFrame con los registros obtenidos.
        """
        records = self.paginator.get_all(
            dataset_id=config.dataset_id,
            params=config.params,
        )

        return pd.DataFrame(records)

    def extract_all(self) -> dict[str, pd.DataFrame]:
        """
        Extrae todos los datasets definidos en el catálogo.

        Returns:
            Diccionario donde la clave es el nombre del dataset
            y el valor es su DataFrame.
        """
        datasets = {}

        for dataset_name, config in DATASETS.items():
            print(f"Extrayendo dataset: {dataset_name}")

            datasets[dataset_name] = self.extract(config)

            print(
                f"Dataset '{dataset_name}': "
                f"{len(datasets[dataset_name])} registros"
            )

        return datasets

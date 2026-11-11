"""
Carga los datasets procesados en Supabase reemplazando sus tablas.
"""

import re

import pandas as pd
from sqlalchemy.engine import Engine

from database.connection import get_engine

_TABLE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")


class DataUploader:
    """Reemplaza las tablas de los datasets procesados en una transacción."""

    def __init__(self, engine: Engine | None = None):
        self.engine = engine

    def upload_all(self, datasets: dict[str, pd.DataFrame]) -> None:
        """
        Recrea una tabla por cada dataset procesado y carga sus registros.

        Todas las tablas se reemplazan en una única transacción. Si una carga
        falla, la base de datos conserva las tablas que tenía antes del lote.
        """
        if not datasets:
            raise ValueError("No hay datasets procesados para cargar.")

        for name, dataframe in datasets.items():
            if not _TABLE_NAME_PATTERN.fullmatch(name):
                raise ValueError(f"Nombre de tabla no válido: {name!r}.")
            if not isinstance(dataframe, pd.DataFrame):
                raise TypeError(
                    f"El dataset {name!r} no es un pandas.DataFrame."
                )

        engine = self.engine if self.engine is not None else get_engine()
        with engine.begin() as connection:
            for name, dataframe in datasets.items():
                dataframe.to_sql(
                    name,
                    con=connection,
                    if_exists="replace",
                    index=False,
                    chunksize=1000,
                )

        for name, dataframe in datasets.items():
            print(f"Tabla '{name}' recreada: {len(dataframe)} registros")

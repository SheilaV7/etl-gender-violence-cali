""" from datetime import datetime

import pandas as pd
from services.api_client import DatosGovClient

def main():

    client = DatosGovClient()

    datos = client.get_dataset(
        "fpe5-yrmw",
        {
            "$where": "municipio='Cali (CT)'",
            "$limit": 30000
        }
    )

    df = pd.DataFrame(datos)

    columnas = client.get_columns("fpe5-yrmw")
    for col in columnas:
        print(col)

    actualizacion = client.get_last_update("fpe5-yrmw")
    print("\nÚltima actualización de datos:",
          datetime.fromtimestamp(actualizacion["datos_actualizados"]))

    print(df['codigo_dane'].nunique())
    print(df['codigo_dane'].unique())

    print(df['cantidad'].nunique())
    print(df['cantidad'].unique())

if __name__ == "__main__":
    main()
 """

"""
Punto de entrada: recorre el catálogo de datasets, extrae, procesa
y guarda el resultado de cada uno.
"""

from services.dataset_extractor import DatasetExtractor


def main():
    extractor = DatasetExtractor()

    datasets = extractor.extract_all()

    for name, df in datasets.items():
        print(f"{name}: {len(df)} registros")


if __name__ == "__main__":
    main()
"""
Punto de entrada: recorre el catálogo de datasets, extrae, procesa
y guarda el resultado de cada uno.
"""

from services.dataset_extractor import DatasetExtractor
from services.preprocessor import Preprocessor


def main():
    datasets = DatasetExtractor().extract_all()
    datasets = Preprocessor().process_all(datasets)

    for name, df in datasets.items():
        print(f"{name}: {len(df)} registros")


if __name__ == "__main__":
    main()

"""
Punto de entrada: recorre el catálogo de datasets, extrae, procesa
y guarda el resultado de cada uno.
"""

from services.dataset_extractor import DatasetExtractor
from services.data_uploader import DataUploader
from services.preprocessor import Preprocessor


def main():
    datasets = DatasetExtractor().extract_all()
    datasets = Preprocessor().process_all(datasets)
    DataUploader().upload_all(datasets)


if __name__ == "__main__":
    main()

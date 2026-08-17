"""
Catálogo de datasets consumidos desde la API de Datos Abiertos Colombia.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DatasetConfig:
    name: str
    dataset_id: str
    params: dict = field(default_factory=dict)
    k_anonimidad: int | None = None


DATASETS: dict[str, DatasetConfig] = {
    "delitos_sexuales": DatasetConfig(
        name="delitos_sexuales",
        dataset_id="fpe5-yrmw",
        params={"$where": "municipio='Cali (CT)'"},
        k_anonimidad=5,
    ),
}

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
    "violencia_intrafamiliar": DatasetConfig(
        name="violencia_intrafamiliar",
        dataset_id="ers2-kerr",
        params={"$where": "municipio_del_hecho_dane='Cali'"},
        k_anonimidad=5,
    ),
    "terrorismo_policia_nacional": DatasetConfig(
        name="terrorismo_policia_nacional",
        dataset_id="37p5-impc",
        params={"$where": "municipio='Cali (CT)'"},
        k_anonimidad=5,
    ),
    "infantes_victimas": DatasetConfig(
        name="infantes_victimas",
        dataset_id="8mcu-22np",
        params={"$where": "municipio='Cali'"},
        k_anonimidad=5,
    ),
    "examenes_violencia_sexual": DatasetConfig(
        name="examenes_violencia_sexual",
        dataset_id="hyqu-diue",
        params={"$where": "municipio_del_hecho_dane='Cali'"},
        k_anonimidad=5,
    ),
    "reporte_hurto_transporte": DatasetConfig(
        name="reporte_hurto_transporte",
        dataset_id="9vha-vh9n",
        params={"$where": "municipio='Cali (CT)'"},
        k_anonimidad=5,
    ),
    "reporte_hurto_abigeato_bancos_pirateria": DatasetConfig(
        name="reporte_hurto_abigeato_bancos_pirateria",
        dataset_id="d4fr-sbn2",
        params={"$where": "municipio='Cali (CT)'"},
        k_anonimidad=5,
    ),
    "reporte_hurto_residencias_comercio": DatasetConfig(
        name="reporte_hurto_residencias_comercio",
        dataset_id="6sqw-8cg5",
        params={"$where": "municipio='Cali (CT)'"},
        k_anonimidad=5,
    ),
    "secuestro": DatasetConfig(
        name="secuestro",
        dataset_id="d7zw-hpf4",
        params={"$where": "municipio='CALI'"},
        k_anonimidad=5,
    ),
    "lesiones_no_fatales": DatasetConfig(
        name="lesiones_no_fatales",
        dataset_id="79dd-d24f",
        params={"$where": "municipio_del_hecho_dane='Cali'"},
        k_anonimidad=5,
    ),
    "violencia_interpersonal": DatasetConfig(
        name="violencia_interpersonal",
        dataset_id="e3xi-4zq5",
        params={"$where": "municipio_del_hecho_dane='Cali'"},
        k_anonimidad=5,
    ),
    "violencia_pareja": DatasetConfig(
        name="violencia_pareja",
        dataset_id="9fs6-37ea",
        params={"$where": "municipio_del_hecho_dane='Cali'"},
        k_anonimidad=5,
    ),
    "presuntos_homicidios": DatasetConfig(
        name="lesiones_no_fatales",
        dataset_id="vtub-3de2",
        params={"$where": "municipio_del_hecho_dane='Cali'"},
        k_anonimidad=5,
    ),
    "lesiones_fatales": DatasetConfig(
        name="lesiones_fatales",
        dataset_id="2kpj-cktv",
        params={"$where": "municipio_del_hecho_dane='Cali'"},
        k_anonimidad=5,
    ),
    "desaparecidos": DatasetConfig(
        name="desaparecidos",
        dataset_id="8hqm-7fdt",
        params={"$where": "municipio_donde_ocurre_la_desaparicion_dane='Cali'"},
        k_anonimidad=5,
    ),
}

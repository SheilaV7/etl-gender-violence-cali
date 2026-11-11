"""
Preprocesamiento posterior a la extracción.

Orden: geografía, fecha, género, cantidad unitaria, edad y las reglas
de cada dataset. Los tres hurtos quedan en un solo dataframe.
"""

import pandas as pd

from config.datasets import DATASETS
from config.metadatos import (
    ARMA_TERRORISMO_AGRUPADA,
    ARMAS_TERRORISMO_CONSERVADAS,
    CLASE_SITIO_AGRUPADA,
    CODIGO_DANE_CALI,
    COLUMNA_EDAD_MAYOR_MENOR,
    COLUMNA_EDAD_QUINQUENAL,
    COLUMNAS_CONSTANTES,
    COLUMNAS_EDAD_OMITIDAS,
    COLUMNAS_GEOGRAFIA_OMITIDAS,
    DATASET_HURTO,
    DATASETS_HURTO,
    EDAD_MAYOR_MENOR,
    EDAD_QUINQUENAL,
    GENERO_NO_REPORTADO,
    MUNICIPIO_CALI,
)

# Policía: fecha_hecho en texto DD/MM/YYYY.
# Infantes y secuestro: ISO. Medicina Legal y desaparecidos ya traen
# año, mes y día de la semana por separado.
FECHA_DMY = {
    "delitos_sexuales": "fecha_hecho",
    "terrorismo_policia_nacional": "fecha_hecho",
    "reporte_hurto_transporte": "fecha_hecho",
    "reporte_hurto_abigeato_bancos_pirateria": "fecha_hecho",
    "reporte_hurto_residencias_comercio": "fecha_hecho",
}
FECHA_ISO = {
    "infantes_victimas": "fecha",
    "secuestro": "fecha_hecho",
}
_PARTES_HECHO = ("a_o_del_hecho", "mes_del_hecho", "dia_del_hecho")
FECHA_PARTES = {
    "violencia_intrafamiliar": _PARTES_HECHO,
    "examenes_violencia_sexual": _PARTES_HECHO,
    "lesiones_no_fatales": _PARTES_HECHO,
    "violencia_interpersonal": _PARTES_HECHO,
    "violencia_pareja": _PARTES_HECHO,
    "presuntos_homicidios": _PARTES_HECHO,
    "lesiones_fatales": _PARTES_HECHO,
    "desaparecidos": (
        "a_o_de_la_desaparicion",
        "mes_de_la_desaparicion",
        "dia_de_la_desaparicion",
    ),
}

MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}
DIAS_SEMANA = (
    "lunes",
    "martes",
    "miércoles",
    "jueves",
    "viernes",
    "sábado",
    "domingo",
)
DIAS = {
    "lunes": "lunes",
    "martes": "martes",
    "miércoles": "miércoles",
    "miercoles": "miércoles",
    "jueves": "jueves",
    "viernes": "viernes",
    "sábado": "sábado",
    "sabado": "sábado",
    "domingo": "domingo",
}

COLUMNAS_CODIGO = ("codigo_dane", "codigo_dane_municipio", "cod_muni")
COLUMNAS_MUNICIPIO = (
    "municipio",
    "municipio_del_hecho_dane",
    "municipio_donde_ocurre_la_desaparicion_dane",
)
ALIASES_MUNICIPIO = {
    "Cali (CT)": MUNICIPIO_CALI,
    "CALI": MUNICIPIO_CALI,
}
FRENTE = ("municipio", "codigo_dane", "anio", "mes", "dia_semana")


class Preprocessor:
    """Aplica las reglas de limpieza y k-anonimato al resultado de la extracción."""

    def process_all(self, datasets: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        """Procesa cada dataset y une los tres reportes de hurto."""
        salida = {}
        hurtos = []

        for nombre, df in datasets.items():
            procesado = self.process(nombre, df)
            if nombre in DATASETS_HURTO:
                hurtos.append(procesado)
            else:
                salida[nombre] = procesado

        if hurtos:
            salida[DATASET_HURTO] = _unir_hurtos(hurtos)

        return _en_orden_de_catalogo(salida)

    def process(self, nombre: str, df: pd.DataFrame) -> pd.DataFrame:
        """Limpia un dataset. No modifica el dataframe de entrada."""
        df = df.copy()
        df = _normalizar_geografia(df)
        df = _normalizar_fecha(nombre, df)
        df = _normalizar_genero(df)
        df = _eliminar_cantidad_unitaria(df)
        df = _normalizar_edad(df)
        df = _reglas_del_dataset(nombre, df)
        return _ordenar(df)


def _normalizar_geografia(df: pd.DataFrame) -> pd.DataFrame:
    omitir = [columna for columna in COLUMNAS_GEOGRAFIA_OMITIDAS if columna in df.columns]
    df = df.drop(columns=omitir)

    es_cali = None
    for columna in COLUMNAS_CODIGO:
        if columna not in df.columns:
            continue
        codigos = (
            df[columna].astype("string").str.replace(r"\.0$", "", regex=True).str.strip()
        )
        mascara = codigos.str.startswith(CODIGO_DANE_CALI).fillna(False)
        df[columna] = codigos.mask(mascara, CODIGO_DANE_CALI)
        es_cali = mascara
        if columna != "codigo_dane":
            df = df.rename(columns={columna: "codigo_dane"})
        break

    for columna in COLUMNAS_MUNICIPIO:
        if columna not in df.columns:
            continue
        municipios = df[columna].replace(ALIASES_MUNICIPIO)
        if es_cali is not None:
            municipios = municipios.mask(es_cali, MUNICIPIO_CALI)
        df[columna] = municipios
        if columna != "municipio":
            df = df.rename(columns={columna: "municipio"})
        break

    for columna in list(df.columns):
        if str(columna).startswith("zona"):
            df[columna] = _compactar_centro_poblado(df[columna])

    return df


def _compactar_centro_poblado(serie: pd.Series) -> pd.Series:
    texto = serie.astype("string").str.replace(r"\s+", " ", regex=True).str.strip()
    return texto.str.replace("Centro poblado(", "Centro poblado (", regex=False)


def _normalizar_fecha(nombre: str, df: pd.DataFrame) -> pd.DataFrame:
    if nombre in FECHA_DMY:
        return _desde_calendario(df, FECHA_DMY[nombre], "%d/%m/%Y")
    if nombre in FECHA_ISO:
        return _desde_calendario(df, FECHA_ISO[nombre], None)
    if nombre in FECHA_PARTES:
        df = _desde_partes(df, *FECHA_PARTES[nombre])
        if nombre == "desaparecidos" and "fecha_de_la_desaparicion" in df.columns:
            df = df.drop(columns="fecha_de_la_desaparicion")
    return df


def _desde_calendario(df: pd.DataFrame, columna: str, formato: str | None) -> pd.DataFrame:
    if columna not in df.columns:
        return df

    fechas = pd.to_datetime(df[columna], format=formato, errors="coerce")
    df["anio"] = fechas.dt.year.astype("Int64")
    df["mes"] = fechas.dt.month.astype("Int64")
    indices = fechas.dt.dayofweek.astype("Int64")
    df["dia_semana"] = indices.map(dict(enumerate(DIAS_SEMANA)))
    return df.drop(columns=columna)


def _desde_partes(df: pd.DataFrame, col_anio: str, col_mes: str, col_dia: str) -> pd.DataFrame:
    if col_anio in df.columns:
        df["anio"] = pd.to_numeric(df[col_anio], errors="coerce").astype("Int64")
    if col_mes in df.columns:
        mes = df[col_mes].astype("string").str.strip().str.lower()
        df["mes"] = mes.map(MESES).astype("Int64")
    if col_dia in df.columns:
        dia = df[col_dia].astype("string").str.strip().str.lower()
        df["dia_semana"] = dia.map(DIAS)

    sobran = [columna for columna in (col_anio, col_mes, col_dia) if columna in df.columns]
    return df.drop(columns=sobran)


def _normalizar_genero(df: pd.DataFrame) -> pd.DataFrame:
    if "genero" not in df.columns:
        return df

    genero = df["genero"].fillna(GENERO_NO_REPORTADO).astype("string").str.strip().str.upper()
    df["genero"] = genero.replace({
        "": GENERO_NO_REPORTADO,
        "NO REPORTA": GENERO_NO_REPORTADO,
    })
    return df


def _eliminar_cantidad_unitaria(df: pd.DataFrame) -> pd.DataFrame:
    if "cantidad" not in df.columns:
        return df

    valores = pd.to_numeric(df["cantidad"], errors="coerce")
    if valores.notna().any() and valores.dropna().eq(1).all():
        return df.drop(columns="cantidad")
    return df


def _renombrar_primera(df: pd.DataFrame, columnas: tuple[str, ...], destino: str) -> pd.DataFrame:
    for columna in columnas:
        if columna in df.columns:
            return df.rename(columns={columna: destino})
    return df


def _normalizar_edad(df: pd.DataFrame) -> pd.DataFrame:
    df = _renombrar_primera(df, EDAD_QUINQUENAL, COLUMNA_EDAD_QUINQUENAL)
    df = _renombrar_primera(df, EDAD_MAYOR_MENOR, COLUMNA_EDAD_MAYOR_MENOR)
    omitir = [columna for columna in COLUMNAS_EDAD_OMITIDAS if columna in df.columns]
    return df.drop(columns=omitir)


def _reglas_del_dataset(nombre: str, df: pd.DataFrame) -> pd.DataFrame:
    omitir = [columna for columna in COLUMNAS_CONSTANTES.get(nombre, ()) if columna in df.columns]
    if omitir:
        df = df.drop(columns=omitir)

    if nombre == "terrorismo_policia_nacional" and "armas_medios" in df.columns:
        conservadas = df["armas_medios"].isin(ARMAS_TERRORISMO_CONSERVADAS)
        df.loc[~conservadas & df["armas_medios"].notna(), "armas_medios"] = (
            ARMA_TERRORISMO_AGRUPADA
        )

    if nombre == "infantes_victimas":
        df = _agrupar_clase_sitio(df)

    return df


def _agrupar_clase_sitio(df: pd.DataFrame) -> pd.DataFrame:
    if "clase_sitio" in df.columns and "zona" in df.columns:
        df = df.drop(columns="zona")

    k = DATASETS["infantes_victimas"].k_anonimidad
    if "clase_sitio" not in df.columns or not k:
        return df

    conteo = df["clase_sitio"].value_counts()
    raras = conteo[conteo < k].index
    df["clase_sitio"] = df["clase_sitio"].where(
        ~df["clase_sitio"].isin(raras),
        CLASE_SITIO_AGRUPADA,
    )
    return df


def _unir_hurtos(partes: list[pd.DataFrame]) -> pd.DataFrame:
    hurto = pd.concat(partes, ignore_index=True)
    if "genero" not in hurto.columns:
        hurto["genero"] = pd.NA
    return _ordenar(_normalizar_genero(hurto))


def _ordenar(df: pd.DataFrame) -> pd.DataFrame:
    frente = [columna for columna in FRENTE if columna in df.columns]
    resto = [columna for columna in df.columns if columna not in frente]
    return df[frente + resto]


def _en_orden_de_catalogo(salida: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    orden = []
    hurto_puesto = False

    for nombre in DATASETS:
        if nombre in DATASETS_HURTO:
            if not hurto_puesto:
                orden.append(DATASET_HURTO)
                hurto_puesto = True
            continue
        orden.append(nombre)

    return {nombre: salida[nombre] for nombre in orden if nombre in salida}

"""
Decisiones de preprocesamiento que no quedan en las columnas finales.
"""

CODIGO_DANE_CALI = "76001"
MUNICIPIO_CALI = "Cali"
GENERO_NO_REPORTADO = "NO REPORTADO"

# El corte ya es Cali. Localidad no trae otro valor que "Sin información".
COLUMNAS_GEOGRAFIA_OMITIDAS = (
    "departamento",
    "departamento_del_hecho_dane",
    "departamento_donde_ocurre_la_desaparicion_dane",
    "cod_depto",
    "codigo_dane_departamento",
    "localidad_del_hecho",
    "localidad_donde_ocurre_la_desaparicion",
)

# Se conservan solo estas dos. El resto de armas_medios de terrorismo en Cali
# (arma de fuego, artefacto incendiario, bicicleta bomba, cilindro bomba,
# combustible, moto bomba, no reportado, papa explosiva, petardo planfetario,
# rocket, sin empleo de armas) se publica como OTRO ARTEFACTO: varias tienen
# menos de 5 casos y, cruzadas con la fecha, quedan por debajo de k=5.
ARMAS_TERRORISMO_CONSERVADAS = (
    "GRANADA DE MANO",
    "ARTEFACTO EXPLOSIVO/CARGA DINAMITA",
)
ARMA_TERRORISMO_AGRUPADA = "OTRO ARTEFACTO"

# Un solo valor en el corte de Cali, por eso la columna no se incluye.
# presuntos_homicidios.manera_de_muerte = "1 Presuntos Homicidios"
# desaparecidos.contexto = "Desaparición"
COLUMNAS_CONSTANTES = {
    "presuntos_homicidios": ("manera_de_muerte",),
    "desaparecidos": ("contexto",),
}

# En infantes, zona duplica clase_sitio. Lo que tenga menos de k casos pasa a OTRO.
CLASE_SITIO_AGRUPADA = "OTRO"

# Los tres reportes se unen en DATASET_HURTO. Los distingue tipo_de_hurto.
DATASETS_HURTO = (
    "reporte_hurto_transporte",
    "reporte_hurto_abigeato_bancos_pirateria",
    "reporte_hurto_residencias_comercio",
)
DATASET_HURTO = "hurto"

# Quinquenal y mayor/menor se conservan. Judicial y ciclo vital no.
EDAD_QUINQUENAL = (
    "grupo_de_edad_quinquenal",
    "grupo_de_edad_de_la_victima",
    "grupo_de_edad_quinquenal_del_desaparecido",
)
EDAD_MAYOR_MENOR = (
    "grupo_mayor_menor_de_edad",
    "grupo_mayor_y_menor_de_edad_del_desaparecido",
)
COLUMNAS_EDAD_OMITIDAS = (
    "grupo_de_edad_judicial",
    "edad_judicial",
    "grupo_de_edad_judicial_del_desaparecido",
    "ciclo_vital",
    "ciclo_vital_del_desaparecido",
)
COLUMNA_EDAD_QUINQUENAL = "grupo_edad_quinquenal"
COLUMNA_EDAD_MAYOR_MENOR = "grupo_mayor_menor"

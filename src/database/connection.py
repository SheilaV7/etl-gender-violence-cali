"""Creación de conexiones a la base de datos configurada."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from config.settings import DB_URL


def get_engine() -> Engine:
    """Crea un engine usando la URL de Supabase configurada en el entorno."""
    if not DB_URL:
        raise RuntimeError(
            "Falta configurar SUPABASE_DB_URL en el archivo .env."
        )

    return create_engine(DB_URL)

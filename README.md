# etl-gender-violence-cali

# Instalación

## 1. Clonar el repositorio

```bash
git clone ...
```

## 2. Crear el entorno virtual

```bash
python -m venv .venv
```

## 3. Activarlo

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 5. Configurar variables de entorno

Copiar

```text
.env.example
```

como

```text
.env
```

Completar `SUPABASE_DB_URL` en `.env` con la URL de conexión PostgreSQL de
Supabase. No publiques ni compartas ese archivo.

## 6. Ejecutar el ETL

```bash
python src/main.py
```

El ETL extrae y procesa los datasets y luego recrea en el esquema por defecto
de PostgreSQL una tabla por cada salida procesada. Los tres reportes de hurtos
se combinan en la tabla `hurto`. La carga reemplaza las tablas del ETL y sus
datos anteriores; las tablas que no forman parte del lote no se modifican.
Todas las tablas se actualizan en una transacción: si falla una carga, se
revierte el lote completo. Al recrearlas, no se conservan índices, restricciones,
políticas RLS ni permisos configurados directamente en las tablas; deben
configurarse de nuevo si se usan.

# my_table.py
# ---------------------------------------------------------
# Genera un archivo TXT con:
# - Todas las tablas de PostgreSQL
# - Todos sus campos
# - Tipo de dato de cada campo
#
# Base de datos:
# gestion_gastronomica
#
# Uso:
# python my_tables.py
#
# Requisitos:
# pip install psycopg2-binary
# ---------------------------------------------------------

import psycopg2
from pathlib import Path

# =========================================================
# CONFIGURACION DB
# =========================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "gestion_gastronomica",
    "user": "postgres",
    "password": "$FrankO80365"
}

# =========================================================
# ARCHIVO OUTPUT
# =========================================================

OUTPUT_FILE = Path("estructura_db.txt")

# =========================================================
# QUERY
# =========================================================

QUERY = """
SELECT
    table_schema,
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY table_schema, table_name, ordinal_position;
"""

# =========================================================
# MAIN
# =========================================================

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute(QUERY)
        rows = cursor.fetchall()

        contenido = []
        tabla_actual = None

        contenido.append("=" * 80)
        contenido.append("ESTRUCTURA DE BASE DE DATOS")
        contenido.append("Base: gestion_gastronomica")
        contenido.append("=" * 80)
        contenido.append("")

        for schema, table, column, data_type, nullable in rows:

            nombre_tabla = f"{schema}.{table}"

            if nombre_tabla != tabla_actual:
                tabla_actual = nombre_tabla

                contenido.append("")
                contenido.append("-" * 80)
                contenido.append(f"TABLA: {nombre_tabla}")
                contenido.append("-" * 80)

            contenido.append(
                f"  - {column:<30} | {data_type:<20} | NULLABLE: {nullable}"
            )

        # Crear o sobrescribir el TXT
        OUTPUT_FILE.write_text(
            "\n".join(contenido),
            encoding="utf-8"
        )

        print(f"\nOK Archivo generado: {OUTPUT_FILE.resolve()}")

    except Exception as e:
        print("\nERROR:")
        print(e)

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


if __name__ == "__main__":
    main()
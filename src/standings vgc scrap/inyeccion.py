import sqlite3
import json
import os

# === CONFIGURACIÓN ===
RUTA_DB = ""
RUTA_JSON = ""

# === FUNCIONES AUXILIARES ===

def get_or_create(cursor, table, column, value):
    cursor.execute(f"SELECT id FROM {table} WHERE {column} = ?", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute(f"INSERT INTO {table} ({column}) VALUES (?)", (value,))
    return cursor.lastrowid

# === INYECCIÓN DE DATOS ===

def inyectar_datos():
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    torneo_nombre = data["torneo"]
    equipos = data["equipos"]

    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    # Insertar torneo
    torneo_id = get_or_create(cursor, "Torneo", "nombre", torneo_nombre)

    for rank_key, pokemons in equipos.items():
        ranking = int(rank_key.replace("Rank_", ""))

        # Crear nuevo equipo
        cursor.execute("INSERT INTO Equipo (nombre_opcional) VALUES (NULL)")
        equipo_id = cursor.lastrowid

        # Insertar en Clasificacion
        cursor.execute("""
            INSERT INTO Clasificacion (torneo_id, equipo_id, ranking)
            VALUES (?, ?, ?)
        """, (torneo_id, equipo_id, ranking))

        for poke in pokemons:
            # Insertar pokemon (catálogo)
            pokemon_id = get_or_create(cursor, "Pokemon", "nombre", poke["pokemon"])

            # Insertar instancia de pokemon
            cursor.execute("""
                INSERT INTO InstanciaPokemon (equipo_id, pokemon_id, habilidad, tera_type, item)
                VALUES (?, ?, ?, ?, ?)
            """, (
                equipo_id,
                pokemon_id,
                poke["habilidad"],
                poke["tera_type"],
                poke["ítem"]
            ))
            instancia_id = cursor.lastrowid

            # Insertar movimientos
            for idx, mov in enumerate(poke["movimientos"]):
                movimiento_id = get_or_create(cursor, "Movimiento", "nombre", mov)
                cursor.execute("""
                    INSERT INTO PokemonMovimiento (instancia_pokemon_id, movimiento_id, orden)
                    VALUES (?, ?, ?)
                """, (instancia_id, movimiento_id, idx + 1))

    # Guardar cambios
    conn.commit()
    conn.close()
    print("Datos inyectados con éxito.")

# === EJECUCIÓN ===
if __name__ == "__main__":
    inyectar_datos()

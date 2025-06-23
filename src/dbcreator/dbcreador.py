import sqlite3

# Ruta para la base de datos SQLite
ruta = "/home/david/clone_vgc/vgc-pokemetrics/data/procesed_data/database"

# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect(ruta + "/vgc_torneos.sql")
cursor = conn.cursor()

# Crear las tablas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Torneo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Equipo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_opcional TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Clasificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    torneo_id INTEGER NOT NULL,
    equipo_id INTEGER NOT NULL,
    ranking INTEGER NOT NULL,
    FOREIGN KEY (torneo_id) REFERENCES Torneo(id),
    FOREIGN KEY (equipo_id) REFERENCES Equipo(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS InstanciaPokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipo_id INTEGER NOT NULL,
    pokemon_id INTEGER NOT NULL,
    habilidad TEXT NOT NULL,
    tera_type TEXT NOT NULL,
    item TEXT NOT NULL,
    FOREIGN KEY (equipo_id) REFERENCES Equipo(id),
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Movimiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PokemonMovimiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instancia_pokemon_id INTEGER NOT NULL,
    movimiento_id INTEGER NOT NULL,
    orden INTEGER NOT NULL CHECK(orden BETWEEN 1 AND 4),
    FOREIGN KEY (instancia_pokemon_id) REFERENCES InstanciaPokemon(id),
    FOREIGN KEY (movimiento_id) REFERENCES Movimiento(id)
);
""")

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos creada con éxito.")

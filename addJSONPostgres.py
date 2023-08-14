import psycopg2
import json

# Funzione per la creazione delle tabelle
def create_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            coordinates GEOMETRY(Polygon, 4326)
        )
    """)
    conn.commit()

# Funzione per l'inserimento dei dati
def load_json_data(conn, file_path, table_name):
    with open(file_path, 'r') as file:
        data = json.load(file)
        cursor = conn.cursor()
        for feature in data['features']:
            coordinates = json.dumps(feature['geometry'])
            cursor.execute(f"""
                INSERT INTO {table_name} (coordinates)
                VALUES (ST_SetSRID(ST_GeomFromGeoJSON('{coordinates}'), 4326))
            """)
        conn.commit()

conn = psycopg2.connect(
    host="localhost",
    database="postgis_progetto",
    user="postgres",
    password="admin"
)

json_files = {
    "Anderlecht": "Anderlecht_streets.json",
    "Belgium": "Belgium_streets.json",
    "Bruxelles": "Bruxelles_streets.json"
}

# Carica le coordinate delle strade da ciascun file JSON nelle rispettive tabelle
for city, json_file in json_files.items():
    table_name = city.lower() + "_streets"
    json_file_path = json_file
    # Viene creata la tabella se non esiste
    create_table(conn, table_name)
    # Vengono caricati i dati dal json
    load_json_data(conn, json_file_path, table_name)

conn.close()
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgis_progetto",
    user="postgres",
    password="admin"
)

# Lista dei percorsi dei file CSV
csv_files = [
    "traffic_data_Bel/Bel_30min_0101_0103_2019.csv",
    "traffic_data_Bel/Bel_30min_0506_1610_2021.csv",
    "traffic_data_Bel/Bel_30min_1303_0606_2021.csv"
]

def create_traffic_data_and_30min_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_data_bel_30min (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            road_id INTEGER,
            vehicle_count INTEGER,
            average_speed FLOAT
        )
    """)
    conn.commit()

# Creazione della tabella traffic_data_and_30min
create_traffic_data_and_30min_table(conn)
cursor = conn.cursor()

for csv_file in csv_files:
    with open(csv_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            timestamp = parts[0]
            road_id = int(float(parts[1]))  # Converto il road_id in intero
            vehicle_count = int(parts[2])
            average_speed = float(parts[3])

            if vehicle_count == 0:
                continue

            # Creazione dell'istruzione INSERT
            insert_query = f"""
                INSERT INTO traffic_data_bel_30min (timestamp, road_id, vehicle_count, average_speed)
                VALUES ('{timestamp}', {road_id}, {vehicle_count}, {average_speed})
            """

            cursor.execute(insert_query)

conn.commit()
conn.close()

print("Dati inseriti nel database con successo!")
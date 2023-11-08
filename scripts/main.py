import whisper_
import data
from sqlalchemy import create_engine, text
import time
import sys

if len(sys.argv) != 3:
    print(f"Se esperaban 2 argumentos, pero se recibieron {len(sys.argv) - 1}.")
    sys.exit(1)

print("#############################################################")
print("(Si introduces un user nuevo se registra automaticamente, si introduces uno ya usado se le sumara la información)")
username_ = sys.argv[1]
username = username_.lower()
print("#############################################################")
print("(Puedes introducir la URL de un video)")
url = sys.argv[2]
print("#############################################################")

# PROGRAMAR QUE UN MISMO USER NO META EL MISMO VIDEO. UN AVISO DICIENDO QUE ESE VIDEO NO SE PUEDE INTRODUCIR

# Parámetros de conexión
host = "localhost"
dbname = "postgres"
user = "postgres"
password = "postgres"
port = "5433"

def is_on_database():
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)

    with engine.connect() as connection:
            # Ejecutar una consulta SELECT
            result = connection.execute(text(f"SELECT * FROM username WHERE username = '{username}';"))
            fetched_results = result.fetchall()

            if fetched_results:  # Si hay resultados
                return True
            else:  # Si no hay resultados
                return False

def register():
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)

    with engine.connect() as connection:
            # Ejecutar una consulta SELECT
            connection.execute(text(f"INSERT INTO public.username (username) VALUES ('{username}');"))
            connection.commit()  # Confirmar la transacción
            

# Si no está en la base de datos, lo registramos
result_is_on_database = is_on_database()

if result_is_on_database == True:
    print(f"Has hecho login con el user {username}")
if result_is_on_database == False:
    print(f"Usuario no encontrado. Creamos uno nuevo: {username}!")
    register()

## Calculo tiempo inicial
start_time = time.time()

# Logica del proceso
if whisper_.is_video_duplicated(url, username):
     print("#################################################################")
     print(f"Para el user {username} el video ya está en la BBDD. Pruebe con otro")
     print("#################################################################")
else:  
    whisper_.download_audio(url, username)
    text = whisper_.convert_audio_transform()
    whisper_.transform_df(text)
    whisper_.drop_original_audio()
    data.data(username)

## Calculo tiempo final

end_time = time.time()
duration_ = end_time - start_time

duration = int(duration_)

if duration_ < 60:
     print(f"El script tardó {duration} segundos en ejecutarse.")
else:
    minutes_ = duration / 60
    minutes = int(minutes_)
    seconds_ = duration % 60
    seconds = int(seconds_)

    print(f"El script tardó {minutes} minutos y {seconds} segundos en ejecutarse.")

import whisper_
import data
from sqlalchemy import create_engine, text
import time

print("#############################################################")
print("(Si introduces un user nuevo se registra automaticamente, si introduces uno ya usado se le sumara la información)")
username_ = input("Introduce tu nombre usuario: ")
username = username_.lower()
print("#############################################################")
print("(Puedes introducir la URL de un video o la URL de una PLAYLIST)")
url = input("Introduce una URL de youtube: ")
print("#############################################################")


# PROGRAMAR FUNCIONALIDAD DE PLAYLISTS
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
            print("Usuario no encontrado. Creamos uno nuevo!")

# Si no está en la base de datos, lo registramos
result_is_on_database = is_on_database()

if result_is_on_database == True:
    print(f"Has hecho login con el user {username}")
if result_is_on_database == False:
    print(f"Registramos un usuario nuevo.")
    register()

## Calculo tiempo inicial
start_time = time.time()

# Logica del proceso
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
from pytube import YouTube
from moviepy.editor import *
from sqlalchemy import create_engine, text
import whisper
import os
import pandas as pd
import string

# Parámetros de conexión
host = "localhost"
dbname = "postgres"
user = "postgres"
password = "postgres"
port = "5433"

def is_video_duplicated(url, username):
    yt = YouTube(url)
    video_title = yt.title

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)

    with engine.connect() as connection:
        # Ejecutar una consulta SELECT
        result = connection.execute(text(f"SELECT * FROM public.videos WHERE username = '{username}' AND name = '{video_title}';"))
        fetched_results = result.fetchall()

        if fetched_results:  # Si hay resultados
            return True

        else:  # Si no hay resultados
            return False

def download_audio(url, username):
    # Crear un objeto YouTube
    yt = YouTube(url)
    video_title = yt.title
    video_length = yt.length
    video_views = yt.views
    video_author = yt.author

    # Obtener solo audio
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Guardamos el audio
    output_path = '../python/audios'

    audio_stream.download(output_path=output_path, filename='audio')

    # Guardamos info del video

    # Crear la conexión
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    engine = create_engine(connection_string)

    with engine.connect() as connection:
        # Introducir nombre y url
        connection.execute(text(f"insert into public.videos (url, name, length, views, author, username) values ('{url}', '{video_title}', '{video_length}', '{video_views}', '{video_author}', '{username}');"))
        connection.commit()  # Confirmar la transacción
        connection.close()

def convert_audio_transform():
        # Ruta del archivo original
    input_audio_path = '../python/audios/audio'

    # Ruta donde se guardará el archivo mp3
    output_audio_path = '../python/audios/audio.mp3'

    # Cargar el archivo de audio
    audio_clip = AudioFileClip(input_audio_path)

    # Guardar el archivo de audio en formato mp3
    audio_clip.write_audiofile(output_audio_path, codec='mp3')

    #######################    04    ##############################
    ####################### Whisper ###############################

    print("################### Comienza whisper #######################")
    # model = whisper.load_model("base", device="CPU")
    model = whisper.load_model("small", device="cpu")
    result = model.transcribe('../python/audios/audio.mp3')

    print("################### Termina whisper #######################")

    return result["text"]

def drop_original_audio():

    file_path = '../python/audios/audio'

    # Eliminar el archivo
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"El archivo {file_path} no existe.")

    #######################    06    ##############################
    ##################### Conversiones ############################

def transform_df(text):

    # Crear una tabla de traducción para eliminar la puntuación
    translator = str.maketrans('', '', string.punctuation)

    # Usar translate() para eliminar la puntuación del texto
    text_no_punctuation = text.translate(translator)

    # Pasar todo a minusculas
    text_lower = text_no_punctuation.lower()

    # Convertir el texto en un array de Strings
    text_array = text_lower.split()

    # Crear un DataFrame a partir del array de strings
    df = pd.DataFrame(text_array, columns=['Word'])

    # Contar la frecuencia de cada palabra
    word_counts = df['Word'].value_counts().reset_index()

    # Renombrar las columnas para reflejar el contenido
    word_counts.columns = ['Word', 'Frequency']

    # Ordenar el DataFrame por la frecuencia de las palabras de mayor a menor
    sorted_word_counts = word_counts.sort_values(by='Frequency', ascending=False)

    # Filtramos solo las palabras que tengan mas de 3 caracteres
    filtered_words = sorted_word_counts.loc[sorted_word_counts['Word'].str.len() > 3]
    print(filtered_words.head(10))

    #######################    07    ##############################
    ###################### Write .csv #############################

    # Guardar en csv
    # Guardar el DataFrame en un archivo CSV en Google Drive
    filtered_words.to_csv('../python/csv/words.csv', index=False)
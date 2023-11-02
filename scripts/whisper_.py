from pytube import YouTube
from moviepy.editor import *
from sqlalchemy import create_engine, text
import whisper
import time
import os
import pandas as pd
import string

#######################    01    ##############################
################## Descargar audio ############################

# Crear un objeto YouTube
url = "https://www.youtube.com/watch?v=REbSqXPW2wU&ab_channel=TheWildProject"
yt = YouTube(url)
video_title = yt.title
video_length = yt.length
video_views = yt.views
video_author = yt.author

# Obtener solo la transmisión de audio de más alta calidad
audio_stream = yt.streams.filter(only_audio=True).first()

# Guardamos el audio
output_path = './audios'

audio_stream.download(output_path=output_path, filename='audio')

#######################    02    ##############################
############## Guardar en BBDD Metadatos ######################

# Parámetros de conexión
host = "localhost"
dbname = "postgres"
user = "postgres"
password = "postgres"
port = "5433"

# Crear la conexión
# connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
# engine = create_engine(connection_string)


# with engine.connect() as connection:
    # Introducir nombre y url
    # connection.execute(text(f"insert into public.videos (url, name, length, views, author)values ('{url}', '{video_title}', '{video_length}', '{video_views}', '{video_author}');"))
    # connection.commit()  # Confirmar la transacción
    # connection.close()

#######################    03    ##############################
################## Convertir audio ############################

# Ruta del archivo original
input_audio_path = './audios/audio'

# Ruta donde se guardará el archivo mp3
output_audio_path = './audios/audio.mp3'

# Cargar el archivo de audio
audio_clip = AudioFileClip(input_audio_path)

# Guardar el archivo de audio en formato mp3
audio_clip.write_audiofile(output_audio_path, codec='mp3')

#######################    04    ##############################
####################### Whisper ###############################
print(os.path.exists('./audios/audio.mp3'))

print("################### Comienza whisper #######################")
model = whisper.load_model("base")
result = model.transcribe('./audios/audio.mp3')

print("################### Termina whisper #######################")

#######################    05    ################################
################## Borrar audio original ########################

file_path = './audios/audio'

# Eliminar el archivo
if os.path.exists(file_path):
    os.remove(file_path)
else:
    print(f"El archivo {file_path} no existe.")

    text = result["text"]  # Tu código existente

#######################    06    ##############################
##################### Conversiones ############################

text = result["text"]  # Tu código existente

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
filtered_words.to_csv('../csv/words.csv', index=False)
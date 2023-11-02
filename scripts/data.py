from pytube import YouTube
from moviepy.editor import *
from sqlalchemy import create_engine, text
import time
import pandas as pd


#######################    01    ##############################
####################### Leer csv ##############################

# Leer un archivo CSV

df = pd.read_csv('./csv/words.csv')

#######################    01    ##############################
################### Escribir en bbdd ##########################

# Parámetros de conexión
host = "localhost"
dbname = "postgres"
user = "postgres"
password = "postgres"
port = "5433"

connection_string = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(connection_string)

for index, row in df.iterrows():
    word = row['Word']
    frequency = row['Frequency']
    with engine.connect() as connection:
        # Ejecutar una consulta SELECT
        result = connection.execute(text(f"SELECT * FROM public.words_frequency WHERE word = '{word}'"))
        fetched_results = result.fetchall()

        if fetched_results:  # Si hay resultados
            # Actualizar la entrada existente
            try:
                connection.execute(text(f"UPDATE words_frequency SET frequency = frequency + {frequency} WHERE word = '{word}'"))
                connection.commit()  # Confirmar la transacción
                print(f"Actualizado: {word} con frecuencia {frequency}")
            except Exception as e:
                print(f"Error al actualizar: {e}")

        else:  # Si no hay resultados
            # Insertar una nueva entrada
            try:
                connection.execute(text(f"INSERT INTO public.words_frequency (word, frequency) VALUES ('{word}', {frequency})"))
                connection.commit()  # Confirmar la transacción
                print(f"Insertado: {word} con frecuencia {frequency}")
            except Exception as e:
                print(f"Error al insertar: {e}")
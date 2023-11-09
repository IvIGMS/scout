from pytube import YouTube
from moviepy.editor import *
from sqlalchemy import create_engine, text
import pandas as pd

def data(username):
    #######################    01    ##############################
    ####################### Leer csv ##############################

    # Leer un archivo CSV

    df = pd.read_csv('../csv/words.csv')

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
            # Insertar una nueva entrada
            try:
                connection.execute(text(f"INSERT INTO public.words_frequency (word, frequency, username) VALUES ('{word}', {frequency}, '{username}')"))
                connection.commit()  # Confirmar la transacción
                print(f"Insertado: {word} con frecuencia {frequency}")
            except Exception as e:
                print(f"Error al insertar: {e}")
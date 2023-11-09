# scout
Python ETL / Whisper / postgres

python 3.12
java 17

En este ETL pasamos de voz a texto el audio de un video de youtube y guardamos las palabras (filtradas bajo mi criterio) en una base de datos para contar cuantas
veces se repiten en el video. La finalidad es poder tener una base de palabras extensa sumando las palabras contadas de varios videos de youtube. Para ello usamos
la API de whisper de OpenAI.

Funcionamiento: solo hay que introducir un nombre de usuario (al que pertenecerán todos los videos que descarguemos en la sesión con ese user) y también habrá que
introducir la URL del video, si ya tenemos ese video vinculado al user introducido no nos dejará cargarlo para que no tengamos nada duplicado como medida de integridad
de nuestros datos, finalmente nos dirá las palabras introducidas en el log junto con el tiempo que ha tardado en realizar el proceso.

Herramientas necesarias:

--Docker (correr la bbdd de postgre, dentro del archivo de credentials_database.txt está lo necesario para crear la bbdd en docker y luego crear las tablas y la consulta SQL)
--env
--Visual Studio Code (buena integración con entornos virtuales de anaconda)
--git (clonar el repositorio)
--Dbeaber (gestor de base de datos)

Instalar proyecto:
-- Hacemos un git clone del repo
-- Creamos la imagen y contenedor en docker con el script que he dejado en credentials_database.txt
-- Creamos la conexion a la bbdd y las tablas del script
-- Dentro de anaconda en environments hacemos click en importar nuevo enviroment y le pasamos el environment.yml y le damos un nombre.
(de esta forma tendremos todas las librerias necesarias para ejecutar la app)
-- Actvamos el nuevo environmente y nos vamos a home y ejecutamos vscode desde anaconda para que coja en entorno automaticamente.
-- Abrimos el directorio de nuestro proyecto y ejecutamos el main.py y hacemos lo que dice.
-- Para ver los datos puedes usar la query que esta en credentials_database.txt o crear las tuyas propias para explorar los datos.











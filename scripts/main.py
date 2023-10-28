import subprocess
import time

def main():

    ## Calculo tiempo inicial
    start_time = time.time()

    # Llamar al primer script secundario
    subprocess.run(["python", "./scripts/whisper_.py"])

    # Llamar al segundo script secundario
    subprocess.run(["python", "./scripts/data.py"])

    end_time = time.time()
    duration_ = end_time - start_time

    duration = int(duration_)

    ## Calculo tiempo final

    if duration_ < 60:
        print(f"El script tardó {duration} segundos en ejecutarse.")
    else:
        minutes_ = duration / 60
        minutes = int(minutes_)
        seconds_ = duration % 60
        seconds = int(seconds_)

        print(f"El script tardó {minutes} minutos y {seconds} segundos en ejecutarse.")

if __name__ == "__main__":
    main()
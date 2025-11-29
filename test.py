import os
import re
import time

def process_file(file_path, file_name, compiled_data):

    with open(file_path, "r", errors="replace") as f:
        for line in f:
            pattern = r"^([0-9A-Za-z]+)\s+(.+?)\s+([A-Z]{3})\s+(\d+)\s+(\d+)\s+(\d+)(?:\s+(999))?\s+(\d{8})$"
            m = re.match(pattern, line.strip())

            if m:
                id_, nombre, cod, c1, c2, c3, c999, fecha = m.groups()              
                c999 = c999 or "" # Convertir None → "" (cadena vacía)

                fields = [id_, nombre, cod, c1, c2, c3, c999, fecha]
                linea_csv = ",".join(fields)
                compiled_data.write(f"{file_name},{linea_csv.rstrip()}\n")


directory = input("Escriba el nombre de la carpeta: ")

with open("compiled_data.csv", "w") as compiled_data:
    compiled_data.write("Nombre del archivo,Contenido\n")

    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        if os.path.isfile(file_path):  # evita directorios
            
            process_file(file_path, file_name, compiled_data)
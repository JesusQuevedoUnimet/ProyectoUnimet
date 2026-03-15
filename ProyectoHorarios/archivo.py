import json
import csv
import requests
from profesor import Profesor
from materia import Materia

def descargar_api():
    """Descarga los datos de la API de Github y crea los objetos."""
    url = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05/main/datos.json"
    print("\nDescargando datos...")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            datos = response.json()
            materias = [Materia(m["codigo"], m["nombre"], m["secciones"]) for m in datos.get("materias", [])]
            profesores = [Profesor(p["cedula"], p["nombre"], p["correo"], p["max_materias"], p["materias_permitidas"]) for p in datos.get("profesores", [])]
            print(">>> Datos descargados exitosamente.")
            return profesores, materias
        else:
            print(">>> Error al acceder a la API.")
            return [], []
    except Exception as e:
        print(f">>> Error de conexión: {e}")
        return [], []

def cargar_csv():
    """Carga un horario desde un archivo CSV."""
    horario = []
    try:
        with open('horario_guardado.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                horario.append({
                    "materia": row["Materia"],
                    "seccion": int(row["Seccion"]),
                    "profesor": row["Profesor"],
                    "bloque": row["Bloque"]
                })
        print(">>> Horario cargado desde CSV exitosamente.")
    except FileNotFoundError:
        print(">>> Error: No se encontró el archivo 'horario_guardado.csv'.")
    return horario

def guardar_csv(horario):
    """Guarda el horario actual en un archivo CSV."""
    if not horario:
        print(">>> No hay horario generado para guardar.")
        return
    try:
        with open('horario_guardado.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Materia", "Seccion", "Profesor", "Bloque"])
            writer.writeheader()
            for clase in horario:
                writer.writerow({
                    "Materia": clase["materia"],
                    "Seccion": clase["seccion"],
                    "Profesor": clase["profesor"],
                    "Bloque": clase["bloque"]
                })
        print(">>> Horario guardado en 'horario_guardado.csv' exitosamente.")
    except Exception as e:
        print(f">>> Error al guardar: {e}")
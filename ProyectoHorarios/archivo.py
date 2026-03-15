import json
import csv
import requests
from profesor import Profesor
from materia import Materia

def descargar_api():
    """Descarga los datos de la API de Github y crea los objetos."""
    urls_materias = [
        "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-1.json",
        "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2526-2.json",
        "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/materias2425-3.json"
    ]
    url_profesores = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-2/refs/heads/main/profesores.json"
    
    profesores_finales = []
    materias_finales = []
    
    print("\nDescargando datos...")
    try:
        # 1. Descargar Profesores
        res_p = requests.get(url_profesores)
        if res_p.status_code == 200:
            datos_p = res_p.json()
            # El JSON del profe es una lista directa [...]
            for p in datos_p:
                # Usamos los nombres exactos que están en su JSON
                ci = p.get("cedula")
                nom = p.get("nombre")
                corr = p.get("correo")
                max_m = p.get("max_materias")
                mats = p.get("materias_permitidas")
                
                if ci and nom:
                    profesores_finales.append(Profesor(str(ci), nom, corr, int(max_m), mats))
        
        # 2. Descargar Materias
        for url in urls_materias:
            res_m = requests.get(url)
            if res_m.status_code == 200:
                datos_m = res_m.json()
                for m in datos_m:
                    cod = m.get("codigo")
                    nom = m.get("nombre")
                    sec = m.get("secciones")
                    if cod and nom:
                        materias_finales.append(Materia(str(cod), nom, int(sec)))

        print(f">>> ÉXITO: Se cargaron {len(profesores_finales)} profesores y {len(materias_finales)} materias.")
        return profesores_finales, materias_finales

    except Exception as e:
        print(f">>> Error de conexión: {e}")
        return [], []

def cargar_csv():
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
        print(">>> Horario cargado desde archivo.")
    except:
        pass
    return horario

def guardar_csv(horario):
    if not horario:
        print(">>> No hay horario para guardar.")
        return
    try:
        with open('horario_guardado.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Materia", "Seccion", "Profesor", "Bloque"])
            writer.writeheader()
            for c in horario:
                writer.writerow({"Materia": c["materia"], "Seccion": c["seccion"], "Profesor": c["profesor"], "Bloque": c["bloque"]})
        print(">>> Guardado exitoso en CSV.")
    except Exception as e:
        print(f">>> Error al guardar: {e}")
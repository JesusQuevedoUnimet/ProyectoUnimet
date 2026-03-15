import matplotlib.pyplot as plt

def modulo_estadisticas(horario, profesores, bloques_horas):
    """Genera gráficas usando Matplotlib."""
    if not horario:
        print(">>> Primero debe generar un horario.")
        return
        
    print("1. Clases por Bloque de Horario")
    print("2. Carga Académica de Profesores")
    opc = input("Opción: ")
    
    if opc == '1':
        conteo_bloques = {b: 0 for b in bloques_horas}
        for c in horario:
            conteo_bloques[c["bloque"]] += 1
            
        nombres = [b.split(' ')[0] + '\n' + b.split(' ')[-1] for b in conteo_bloques.keys()]
        valores = list(conteo_bloques.values())
        
        plt.figure(figsize=(10, 5))
        plt.bar(nombres, valores, color='skyblue')
        plt.title('Número de Clases por Bloque de Horario')
        plt.xlabel('Bloques')
        plt.ylabel('Cantidad de Clases')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    elif opc == '2':
        conteo_prof = {}
        for c in horario:
            prof = next((p for p in profesores if p.cedula == c["profesor"]), None)
            nombre = prof.nombre if prof else c["profesor"]
            conteo_prof[nombre] = conteo_prof.get(nombre, 0) + 1
            
        plt.figure(figsize=(8, 8))
        plt.pie(conteo_prof.values(), labels=conteo_prof.keys(), autopct='%1.1f%%', startangle=140)
        plt.title('Distribución de Carga por Profesores')
        plt.show()
    else:
         print(">>> Opción inválida.")
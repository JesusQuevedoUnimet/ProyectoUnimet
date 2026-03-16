#Jesus Quevedo y Santiago Arrieta
def generar_horario(profesores, materias, bloques_horas, num_salones):
    """
    Algoritmo Greedy para asignar profesores a materias sin choques.
    Eficiencia: O(m * s * p * b)
    """
    print("\n--- GENERACIÓN DE HORARIOS ---")
    horario = []
    
    # Reiniciar contadores de materias asignadas
    for p in profesores:
        p.materias_asignadas = 0

    materias_cerradas = []
    secciones_sin_asignar = 0

    for materia in materias:
        if materia.secciones == 0:
            continue

        for seccion in range(1, materia.secciones + 1):
            asignado = False
            
            # Buscar profesor apto y con disponibilidad
            profesores_aptos = [p for p in profesores if materia.codigo in p.materias_permitidas and p.materias_asignadas < p.max_materias]
            
            if not profesores_aptos:
                if materia.codigo not in materias_cerradas:
                    materias_cerradas.append(materia.codigo)
                secciones_sin_asignar += 1
                continue

            for prof in profesores_aptos:
                if asignado: break
                for bloque in bloques_horas:
                    clases_en_bloque = len([c for c in horario if c["bloque"] == bloque])
                    if clases_en_bloque >= num_salones:
                        continue
                    
                    choque = any(c["profesor"] == prof.cedula and c["bloque"] == bloque for c in horario)
                    if not choque:
                        horario.append({
                            "materia": materia.codigo,
                            "seccion": seccion,
                            "profesor": prof.cedula,
                            "bloque": bloque
                        })
                        prof.materias_asignadas += 1
                        asignado = True
                        break
            
            if not asignado:
                secciones_sin_asignar += 1

    print("\n>>> HORARIO GENERADO EXITOSAMENTE <<<")
    print(f"Materias cerradas por falta de profesores: {', '.join(materias_cerradas) if materias_cerradas else 'Ninguna'}")
    print(f"Secciones sin asignar (por falta de salones o profes libres): {secciones_sin_asignar}")
    
    return horario
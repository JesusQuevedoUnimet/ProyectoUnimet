#Jesus Quevedo y Santiago Arrieta
def modificar_horario(horario, profesores, bloques_horas, num_salones):
    """Permite cambiar el profesor o el horario de una sección."""
    if not horario:
        print(">>> Primero debe generar o cargar un horario.")
        return horario
        
    codigo = input("Ingrese el código de la materia a modificar: ")
    try:
        seccion = int(input("Ingrese el número de la sección: "))
    except ValueError:
        print(">>> Error: Debe ingresar un número entero.")
        return horario
    
    clase_actual = None
    for c in horario:
        if c["materia"] == codigo and c["seccion"] == seccion:
            clase_actual = c
            break
            
    if not clase_actual:
        print(">>> No se encontró esa clase en el horario actual.")
        return horario
        
    print(f"\nClase encontrada: {clase_actual['materia']} Sec.{clase_actual['seccion']} - Prof: {clase_actual['profesor']} - Bloque: {clase_actual['bloque']}")
    print("1. Cambiar Profesor")
    print("2. Cambiar Bloque de Horario")
    
    opc = input("Opción: ")
    
    if opc == '1':
        nueva_ci = input("Ingrese CI del nuevo profesor: ")
        nuevo_prof = next((p for p in profesores if p.cedula == nueva_ci), None)
        if nuevo_prof and codigo in nuevo_prof.materias_permitidas:
            choque = any(c["profesor"] == nueva_ci and c["bloque"] == clase_actual["bloque"] for c in horario)
            if choque:
                print(">>> Error: El nuevo profesor ya tiene clase en ese bloque.")
            else:
                clase_actual["profesor"] = nueva_ci
                print(">>> Profesor modificado exitosamente.")
        else:
            print(">>> Profesor no encontrado o no está habilitado para esta materia.")
            
    elif opc == '2':
        print("\nBloques disponibles:")
        for i, b in enumerate(bloques_horas): print(f"{i}. {b}")
        try:
            idx_bloque = int(input("Seleccione el ID del nuevo bloque: "))
            if 0 <= idx_bloque < len(bloques_horas):
                nuevo_bloque = bloques_horas[idx_bloque]
                choque = any(c["profesor"] == clase_actual["profesor"] and c["bloque"] == nuevo_bloque for c in horario)
                clases_en_bloque = len([c for c in horario if c["bloque"] == nuevo_bloque])
                
                if choque:
                    print(">>> Error: El profesor ya tiene clase en ese bloque.")
                elif clases_en_bloque >= num_salones:
                    print(">>> Error: No hay salones disponibles en ese bloque.")
                else:
                    clase_actual["bloque"] = nuevo_bloque
                    print(">>> Bloque modificado exitosamente.")
            else:
                print(">>> Bloque inválido.")
        except ValueError:
             print(">>> Error: Debe ingresar un número válido.")
    else:
        print(">>> Opción inválida.")
        
    return horario
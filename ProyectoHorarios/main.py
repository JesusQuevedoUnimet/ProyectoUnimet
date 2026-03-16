#Jesus Quevedo y Santiago Arrieta

# IMPORTAMOS NUESTROS MÓDULOS
from profesor import Profesor
from materia import Materia
import archivo
import generador
import modificador
import estadisticas

class Sistema:
    def __init__(self):
        self.profesores = []
        self.materias = []
        self.horario = []
        self.bloques_horas = [
            "Lunes y Miércoles 7:00-8:30", "Lunes y Miércoles 8:45-10:15", 
            "Lunes y Miércoles 10:30-12:00", "Lunes y Miércoles 12:15-13:45",
            "Martes y Jueves 7:00-8:30", "Martes y Jueves 8:45-10:15", 
            "Martes y Jueves 10:30-12:00", "Martes y Jueves 12:15-13:45",
            "Viernes 7:00-8:30", "Viernes 8:45-10:15", "Viernes 10:30-12:00"
        ]
        self.num_salones = 0

    def pedir_entero(self, mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print(">>> Error: Por favor ingrese un número entero válido.")

    def iniciar(self):
        while True:
            print("\n" + "="*40)
            print("   SISTEMA DE HORARIOS - INICIO")
            print("="*40)
            print("1. Crear listas en blanco")
            print("2. Descargar datos de la API de Github")
            print("3. Cargar un horario en CSV")
            print("4. Salir")
            
            opcion = self.pedir_entero("Seleccione una opción: ")

            if opcion == 1:
                self.profesores, self.materias, self.horario = [], [], []
                self.menu_principal()
            elif opcion == 2:
                self.profesores, self.materias = archivo.descargar_api()
                self.menu_principal()
            elif opcion == 3:
                self.horario = archivo.cargar_csv()
                self.menu_principal()
            elif opcion == 4:
                print("Saliendo del sistema...")
                break
            else:
                print(">>> Opción inválida.")

    def menu_principal(self):
        while True:
            print("\n" + "="*40)
            print("   MÓDULOS FUNDAMENTALES")
            print("="*40)
            print("1. Profesores")
            print("2. Materias")
            print("3. Generación de horarios")
            print("4. Modificación de horarios")
            print("5. Estadísticas")
            print("6. Guardar horario en CSV")
            print("7. Volver al inicio")
            
            opcion = self.pedir_entero("Seleccione un módulo: ")
            
            if opcion == 1: self.menu_profesores()
            elif opcion == 2: self.menu_materias()
            elif opcion == 3: 
                self.num_salones = self.pedir_entero("Ingrese la cantidad de salones disponibles por bloque: ")
                self.horario = generador.generar_horario(self.profesores, self.materias, self.bloques_horas, self.num_salones)
            elif opcion == 4: self.horario = modificador.modificar_horario(self.horario, self.profesores, self.bloques_horas, self.num_salones)
            elif opcion == 5: estadisticas.modulo_estadisticas(self.horario, self.profesores, self.bloques_horas)
            elif opcion == 6: archivo.guardar_csv(self.horario)
            elif opcion == 7: break
            else: print(">>> Opción inválida.")

    # =============== MENÚS DE PROFESORES Y MATERIAS ===============
    
    def buscar_profesor_por_cedula(self, cedula):
        for p in self.profesores:
            if p.cedula == cedula: return p
        return None

    def buscar_materia_por_codigo(self, codigo):
        for m in self.materias:
            if m.codigo == codigo: return m
        return None

    def menu_profesores(self):
        while True:
            print("\n--- MÓDULO DE PROFESORES ---")
            print("1. Ver la lista de profesores")
            print("2. Ver un profesor específico")
            print("3. Agregar un profesor")
            print("4. Eliminar un profesor")
            print("5. Modificar materias de un profesor")
            print("6. Volver")
            opc = self.pedir_entero("Opción: ")
            
            if opc == 1:
                for p in self.profesores: print(p)
            elif opc == 2:
                ced = input("CI: ")
                p = self.buscar_profesor_por_cedula(ced)
                if p: print(f"{p}\nMaterias: {p.materias_permitidas}")
                else: print(">>> No encontrado.")
            elif opc == 3:
                ced = input("Cédula: ")
                if not self.buscar_profesor_por_cedula(ced):
                    nom = input("Nombre: ")
                    corr = input("Correo: ")
                    max_mat = self.pedir_entero("Máx materias: ")
                    mat_perm = input("Materias permitidas (separadas por coma): ").split(',')
                    mat_perm = [m.strip() for m in mat_perm if m.strip()]
                    self.profesores.append(Profesor(ced, nom, corr, max_mat, mat_perm))
                    print(">>> Agregado exitosamente.")
                else: print(">>> Ya existe esa CI.")
            elif opc == 4:
                ced = input("Cédula a eliminar: ")
                p = self.buscar_profesor_por_cedula(ced)
                if p:
                    mat_afectadas = [c for c in p.materias_permitidas if not [pr for pr in self.profesores if c in pr.materias_permitidas and pr.cedula != ced]]
                    if mat_afectadas:
                        if input(f"ADVERTENCIA: Dejará sin profesor a {mat_afectadas}. ¿Eliminar? (s/n): ").lower() != 's': continue
                    self.profesores.remove(p)
                    print(">>> Eliminado.")
            elif opc == 5:
                # Logica simplificada de modificacion por espacio
                ced = input("Cédula: ")
                p = self.buscar_profesor_por_cedula(ced)
                if p:
                    acc = input("A) Agregar o B) Quitar materia (A/B): ").upper()
                    cod = input("Código de materia: ")
                    if acc == 'A' and cod not in p.materias_permitidas: p.materias_permitidas.append(cod)
                    elif acc == 'B' and cod in p.materias_permitidas: p.materias_permitidas.remove(cod)
            elif opc == 6: break

    def menu_materias(self):
        while True:
            print("\n--- MÓDULO DE MATERIAS ---")
            print("1. Ver la lista de materias")
            print("2. Ver los detalles de una materia")
            print("3. Agregar una materia")
            print("4. Eliminar una materia")
            print("5. Modificar secciones")
            print("6. Volver")
            opc = self.pedir_entero("Opción: ")
            
            if opc == 1:
                for m in self.materias: print(m)
            elif opc == 2:
                cod = input("Código: ")
                m = self.buscar_materia_por_codigo(cod)
                if m: print(m)
                else: print(">>> No encontrada.")
            elif opc == 3:
                cod = input("Código nuevo: ")
                if not self.buscar_materia_por_codigo(cod):
                    nom = input("Nombre: ")
                    sec = self.pedir_entero("Secciones: ")
                    self.materias.append(Materia(cod, nom, sec))
                    print(">>> Agregada.")
                else: print(">>> Ya existe.")
            elif opc == 4:
                cod = input("Código a eliminar: ")
                m = self.buscar_materia_por_codigo(cod)
                if m:
                    self.materias.remove(m)
                    for p in self.profesores:
                        if cod in p.materias_permitidas: p.materias_permitidas.remove(cod)
                    print(">>> Eliminada.")
            elif opc == 5:
                cod = input("Código: ")
                m = self.buscar_materia_por_codigo(cod)
                if m:
                    ns = self.pedir_entero("Nuevas secciones (0 cancela oferta): ")
                    if ns == 0 and input("ADVERTENCIA: Fijar en 0 cancela la oferta. ¿Continuar? (s/n): ").lower() != 's': continue
                    m.secciones = ns
            elif opc == 6: break

if __name__ == "__main__":
    app = Sistema()
    app.iniciar()
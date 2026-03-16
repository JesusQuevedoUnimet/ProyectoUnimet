#Jesus Quevedo y Santiago Arrieta
class Profesor:
    """Representa a un profesor dentro del sistema."""
    def __init__(self, cedula, nombre, correo, max_materias, materias_permitidas):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.max_materias = max_materias
        self.materias_permitidas = materias_permitidas 
        self.materias_asignadas = 0  # Contador para la generación de horarios

    def __str__(self):
        return f"{self.nombre} (CI: {self.cedula}) - Max: {self.max_materias} - Asignadas: {self.materias_asignadas}"
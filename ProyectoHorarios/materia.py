#Jesus Quevedo y Santiago Arrieta
class Materia:
    """Representa una materia dentro del sistema."""
    def __init__(self, codigo, nombre, secciones):
        self.codigo = codigo
        self.nombre = nombre
        self.secciones = secciones

    def __str__(self):
        return f"[{self.codigo}] {self.nombre} - Secciones: {self.secciones}"
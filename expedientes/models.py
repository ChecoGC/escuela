from django.db import models

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.matricula})"


class Documento(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="documentos")
    archivo = models.FileField(upload_to="documentos/")

    def __str__(self):
        return f"Documento de {self.estudiante.nombre}"

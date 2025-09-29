from django import forms
from .models import Estudiante, Documento

# Formulario para crear un estudiante
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ["nombre", "matricula"]


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["archivo"]  

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# Formulario para subir múltiples archivos
class MultipleUploadForm(forms.Form):
    archivos = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True}),
        required=True,
        label="Archivos"
    )

    def clean_archivos(self):
        archivos = self.files.getlist("archivos")
        if not archivos:
            raise forms.ValidationError("Debe seleccionar al menos un archivo.")

        for archivo in archivos:
            if archivo.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
                raise forms.ValidationError(
                    f"El archivo {archivo.name} no es válido. Solo se permiten PDF o imágenes (JPG, PNG)."
                )
        return archivos

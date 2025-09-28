from django import forms
from .models import Estudiante, Documento

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ["nombre", "matricula"]


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ["archivo"]

    def clean_archivo(self):
        archivo = self.cleaned_data.get("archivo")
        if archivo:
            if not archivo.content_type in ["application/pdf", "image/jpeg", "image/png"]:
                raise forms.ValidationError("Solo se permiten archivos PDF o imágenes (JPG, PNG).")
        return archivo


# Formulario para subir múltiples archivos
class MultipleUploadForm(forms.Form):
    archivos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_archivos(self):
        archivos = self.files.getlist("archivos")
        for archivo in archivos:
            if not archivo.content_type in ["application/pdf", "image/jpeg", "image/png"]:
                raise forms.ValidationError(f"El archivo {archivo.name} no es válido (solo PDF o imágenes).")
        return archivos

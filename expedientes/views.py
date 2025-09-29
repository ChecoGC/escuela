from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Estudiante, Documento
from .forms import EstudianteForm, MultipleUploadForm

# Lista de estudiantes
class EstudianteListView(ListView):
    model = Estudiante
    template_name = "expedientes/estudiante_list.html"

# Crear estudiante
class EstudianteCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "expedientes/estudiante_form.html"
    success_url = reverse_lazy("expediente_list")

# Detalle de estudiante
class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = "expedientes/estudiante_detail.html"

def subir_documentos(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)

    if request.method == "POST":
        archivos = request.FILES.getlist("archivos")  # 🔹 obtener la lista directamente

        if not archivos:
            return render(request, "expedientes/subir_documentos.html", {
                "error": "Debe seleccionar al menos un archivo.",
                "estudiante": estudiante
            })

        # Validar tipo de archivo
        for archivo in archivos:
            if archivo.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
                return render(request, "expedientes/subir_documentos.html", {
                    "error": f"El archivo {archivo.name} no es válido (solo PDF o imágenes).",
                    "estudiante": estudiante
                })

        # Guardar archivos
        for archivo in archivos:
            Documento.objects.create(estudiante=estudiante, archivo=archivo)

        return redirect("expediente_detail", pk=estudiante.pk)

    return render(request, "expedientes/subir_documentos.html", {"estudiante": estudiante})


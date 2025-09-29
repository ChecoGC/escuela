from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Estudiante, Documento
from .forms import EstudianteForm, DocumentoForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DocumentoForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.estudiante = self.object
            documento.save()
            return redirect("estudiante_detail", pk=self.object.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

# Subir múltiples documentos
def subir_documentos(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)

    if request.method == "POST":
        archivos = request.FILES.getlist("archivos")

        if not archivos:
            return render(request, "expedientes/subir_documentos.html", {
                "error": "Debe seleccionar al menos un archivo.",
                "estudiante": estudiante
            })

        # Validar tipos de archivo
        for archivo in archivos:
            if archivo.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
                return render(request, "expedientes/subir_documentos.html", {
                    "error": f"El archivo {archivo.name} no es válido (solo PDF o imágenes).",
                    "estudiante": estudiante
                })

        # Guardar archivos
        for archivo in archivos:
            Documento.objects.create(estudiante=estudiante, archivo=archivo)

        return redirect("estudiante_detail", pk=estudiante.pk)

    return render(request, "expedientes/subir_documentos.html", {"estudiante": estudiante})

def eliminar_documento(request, estudiante_pk, doc_pk):
    documento = get_object_or_404(Documento, pk=doc_pk, estudiante__pk=estudiante_pk)
    if request.method == "POST":
        if documento.archivo:
            documento.archivo.delete(save=False)
        documento.delete()
        return redirect("estudiante_detail", pk=documento.estudiante.pk)  # 👈 usamos el pk real
    return render(request, "expedientes/eliminar_documento.html", {"documento": documento})

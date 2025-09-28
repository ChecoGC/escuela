from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from .models import Estudiante, Documento
from .forms import EstudianteForm, MultipleUploadForm


class EstudianteListView(ListView):
    model = Estudiante
    template_name = "expedientes/estudiante_list.html"


class EstudianteCreateView(CreateView):
    model = Estudiante
    form_class = EstudianteForm
    template_name = "expedientes/estudiante_form.html"
    success_url = reverse_lazy("expediente_list")


class EstudianteDetailView(DetailView):
    model = Estudiante
    template_name = "expedientes/estudiante_detail.html"


def subir_documentos(request, pk):
    estudiante = Estudiante.objects.get(pk=pk)

    if request.method == "POST":
        form = MultipleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivos = request.FILES.getlist("archivos")
            for archivo in archivos:
                Documento.objects.create(estudiante=estudiante, archivo=archivo)
            return redirect("expediente_detail", pk=estudiante.pk)
    else:
        form = MultipleUploadForm()

    return render(request, "expedientes/subir_documentos.html", {"form": form, "estudiante": estudiante})

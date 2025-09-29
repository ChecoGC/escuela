from django.urls import path
from .views import EstudianteListView, EstudianteCreateView, EstudianteDetailView, subir_documentos, eliminar_documento

urlpatterns = [
    path("", EstudianteListView.as_view(), name="expediente_list"),
    path("nuevo/", EstudianteCreateView.as_view(), name="expediente_create"),
    path("<int:pk>/", EstudianteDetailView.as_view(), name="estudiante_detail"),
    path("<int:pk>/subir/", subir_documentos, name="subir_documentos"),
    path("<int:estudiante_pk>/documento/<int:doc_pk>/eliminar/", eliminar_documento, name="eliminar_documento"),
]

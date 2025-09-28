from django.urls import path
from .views import EstudianteListView, EstudianteCreateView, EstudianteDetailView, subir_documentos

urlpatterns = [
    path("", EstudianteListView.as_view(), name="expediente_list"),
    path("nuevo/", EstudianteCreateView.as_view(), name="expediente_create"),
    path("<int:pk>/", EstudianteDetailView.as_view(), name="expediente_detail"),
    path("<int:pk>/subir/", subir_documentos, name="subir_documentos"),
]

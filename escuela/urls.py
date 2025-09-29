from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin de Django
    path("expedientes/", include("expedientes.urls")),  # Nuestra app
    path("", RedirectView.as_view(url="/expedientes/")),  # Redirige la raíz a expedientes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

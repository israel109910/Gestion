from django.contrib import admin
from django.urls import path, include  # ← Asegúrate de tener esto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Instrumentos.urls')),
    path('gasolina/', include('Gasolina.urls')),
]
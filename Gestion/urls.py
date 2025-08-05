from django.contrib import admin
from django.urls import path, include  # <- ¡aquí está el fix!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Instrumentos.urls')),  # rutas de tu app principal
    path('gasolina/', include('Gasolina.urls')),  # rutas de la app de gasolina
]

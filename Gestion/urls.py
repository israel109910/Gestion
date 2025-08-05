from django.contrib import admin
from django.urls import path, include  # ← Asegúrate de importar `include`

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Instrumentos.urls')),  # Página principal
    path('gasolina/', include('Gasolina.urls')),  # ← esta es la que fallaba
]

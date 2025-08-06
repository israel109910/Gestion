from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from Instrumentos import views as instrumentos_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', instrumentos_views.inicio, name='home'),  # Página principal
    path('instrumentos/', include(('Instrumentos.urls', 'instrumentos'), namespace='instrumentos')),
    path('gasolina/', include(('Gasolina.urls', 'gasolina'), namespace='gasolina')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]

# Gasolina/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.calcular_viaticos, name='gasolina_index'),
]

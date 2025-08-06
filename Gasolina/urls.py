# Gasolina/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.calcular_viaticos, name='gasolina_index'),
    path('descargar-pdf/', views.descargar_viaticos_pdf, name='descargar_viaticos_pdf'),
]
